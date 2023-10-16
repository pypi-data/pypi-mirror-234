from __future__ import annotations

import json
import uuid
from typing import List
from mongoengine.connection import get_db
import math
from mlflow.entities import (
    Experiment,
    RunTag,
    Metric,
    Param,
    Run,
    RunStatus,
    LifecycleStage,
    ViewType,
    SourceType,
)
from mlflow.protos.databricks_pb2 import (
    INVALID_PARAMETER_VALUE,
    INVALID_STATE,
    RESOURCE_DOES_NOT_EXIST,
    RESOURCE_ALREADY_EXISTS,
)
from mlflow.store.entities import PagedList
from mlflow.store.model_registry import DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH
from mlflow.store.tracking import (
    SEARCH_MAX_RESULTS_DEFAULT,
    SEARCH_MAX_RESULTS_THRESHOLD,
)
from mlflow.store.tracking.abstract_store import AbstractStore
from mlflow.utils.file_utils import local_file_uri_to_path, mkdir
from mlflow.utils.mlflow_tags import (
    _get_run_name_from_tags,
    MLFLOW_RUN_NAME,
    MLFLOW_LOGGED_MODELS,
)
from mlflow.utils.name_utils import _generate_random_name
from mongoengine import connect, BulkWriteError
from mongoengine.queryset.visitor import Q
from six.moves import urllib

from mlflow.exceptions import MlflowException
from mlflow.utils.uri import append_to_uri_path, resolve_uri_if_local, is_local_uri
from mlflow.utils.search_utils import SearchUtils, SearchExperimentsUtils
from mlflow.utils.validation import (
    _validate_batch_log_limits,
    _validate_batch_log_data,
    _validate_run_id,
    _validate_experiment_name,
    _validate_experiment_tag,
    _validate_metric,
    _validate_param_keys_unique,
    _validate_tag,
    _validate_param,
)
from mlflow.utils.time_utils import get_current_time_millis

from .models import (
    MongoExperiment,
    MongoRun,
    MongoMetric,
    MongoParam,
    MongoTag,
    MongoExperimentTag,
    SequenceId,
    MongoLatestMetric,
    _get_next_exp_id,
)

RunStatusTypes = [
    RunStatus.to_string(RunStatus.SCHEDULED),
    RunStatus.to_string(RunStatus.FAILED),
    RunStatus.to_string(RunStatus.FINISHED),
    RunStatus.to_string(RunStatus.RUNNING),
    RunStatus.to_string(RunStatus.KILLED),
]


def _like_to_regex(like_pattern: str):
    """
    Convert a SQL LIKE pattern to a regex pattern.

    :param like_pattern: The SQL LIKE pattern to be converted.
    :return: A string representing the regex pattern equivalent of the input."""
    like_pattern = "^" + like_pattern + "$"
    return like_pattern.replace("%", ".*")


def _get_filter_query(attr, comp, value):
    """
    Generate a query filter using the attribute, comparator, and value.

    :param attr: The attribute to compare.
    :param comp: The comparison operator, as a string.
    :param value: The value to compare the attribute with.
    :return: A Q object representing the query filter.
    """
    if comp == ">":
        return Q(**{f"{attr}__gt": value})
    elif comp == ">=":
        return Q(**{f"{attr}__gte": value})
    elif comp == "!=":
        return Q(**{f"{attr}__ne": value})
    elif comp == "=":
        return Q(**{f"{attr}": value})
    elif comp == "<":
        return Q(**{f"{attr}__lt": value})
    elif comp == "<=":
        return Q(**{f"{attr}__lte": value})
    elif comp == "LIKE":
        return Q(**{f"{attr}__regex": _like_to_regex(value)})
    elif comp == "ILIKE":
        return Q(**{f"{attr}__iregex": _like_to_regex(value)})
    elif comp == "IN":
        return Q(**{f"{attr}__in": value})
    elif comp == "NOT IN":
        return Q(**{f"{attr}__nin": value})


def _get_list_contains_query(key, val, comp, list_field_name):
    """
    Generate a query filter for a list using the key, value, comparator, and list field name.

    :param key: The key to compare.
    :param val: The value to compare with the key.
    :param comp: The comparison operator, as a string.
    :param list_field_name: The name of the field containing the list.
    :return: A Q object representing the query filter.
    """
    value_filter = {}

    if comp == ">":
        value_filter = {"$gt": val}
    elif comp == ">=":
        value_filter = {"$gte": val}
    elif comp == "!=":
        value_filter = {"$ne": val}
    elif comp == "=":
        value_filter = val
    elif comp == "<":
        value_filter = {"$lt": val}
    elif comp == "<=":
        value_filter = {"$lte": val}
    elif comp == "LIKE":
        value_filter = {"$regex": _like_to_regex(val)}
    elif comp == "ILIKE":
        value_filter = {"$regex": _like_to_regex(val), "$options": "i"}

    return Q(**{f"{list_field_name}__match": {"key": key, "value": value_filter}})


def _get_metrics_contains_query(key, val, comp):
    """
    Generate a query filter for metrics using the key, value, and comparator.

    :param key: The key to compare.
    :param val: The value to compare with the key.
    :param comp: The comparison operator, as a string.
    :return: A Q object representing the query filter.
    """
    value_filter = {}

    if comp == ">":
        value_filter = "__gt"
    elif comp == ">=":
        value_filter = "__gte"
    elif comp == "!=":
        value_filter = "__ne"
    elif comp == "=":
        value_filter = ""
    elif comp == "<":
        value_filter = "__lt"
    elif comp == "<=":
        value_filter = "__lte"
    return Q(**{"latest_metrics__match": {"key": key, f"value{value_filter}": val}})


def _order_by_clause(key, ascending):
    """
    Generate an order by clause for a given key and sort order.

    :param key: The key to sort by.
    :param ascending: A boolean indicating whether the sort should be in ascending order.
    :return: A string representing the order by clause.
    """
    if ascending:
        return f"+{key}"
    return f"-{key}"


def _get_search_experiments_filter_clauses(parsed_filters):
    """
    Generate a query filter for search experiments using parsed filters.

    :param parsed_filters: A list of dictionaries, each containing a type, key, comparator, and value.
    :return: A Q object representing the query filter.
    """
    _filter = Q()
    for f in parsed_filters:
        type_ = f["type"]
        key = f["key"]
        comparator = f["comparator"]
        value = f["value"]
        if type_ == "attribute":
            if SearchExperimentsUtils.is_string_attribute(
                type_, key, comparator
            ) and comparator not in ("=", "!=", "LIKE", "ILIKE"):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for string attribute: {comparator}"
                )
            if SearchExperimentsUtils.is_numeric_attribute(
                type_, key, comparator
            ) and comparator not in ("=", "!=", "<", "<=", ">", ">="):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for numeric attribute: {comparator}"
                )
            _filter &= _get_filter_query(key, comparator, value)
        elif type_ == "tag":
            if comparator not in ("=", "!=", "LIKE", "ILIKE"):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for tag: {comparator}"
                )
            _filter &= _get_list_contains_query(
                key=key, val=value, comp=comparator, list_field_name="tags"
            )
        else:
            raise MlflowException.invalid_parameter_value(
                f"Invalid token type: {type_}"
            )

    return _filter


def _get_search_experiments_order_by_clauses(order_by):
    """
    Generate a list of order by clauses for search experiments using an input order by list.

    :param order_by: A list of strings, each representing a field to order by and the order (ascending or descending).
    :return: A list of strings, each representing an order by clause.
    """
    order_by_clauses = []
    for type_, key, ascending in map(
        SearchExperimentsUtils.parse_order_by_for_search_experiments,
        order_by or ["creation_time DESC", "experiment_id ASC"],
    ):
        if type_ == "attribute":
            order_by_clauses.append((key, ascending))
        else:
            raise MlflowException.invalid_parameter_value(
                f"Invalid order_by entity: {type_}"
            )

    # Add a tie-breaker
    if not any(col == "experiment_id" for col, _ in order_by_clauses):
        order_by_clauses.append(("experiment_id", False))

    return [_order_by_clause(col, ascending) for col, ascending in order_by_clauses]


def _get_search_run_filter_clauses(parsed_filters):
    """
    Generate a search filter for run based on the parsed filters.

    :param parsed_filters: A list of dictionaries. Each dictionary represents a filter with keys 'type', 'key', 'comparator', and 'value'.
    :return: A combined filter (a Q object) based on the input parsed filters.
    """
    _filter = Q()

    for f in parsed_filters:
        type_ = f.get("type")
        key = f.get("key")
        value = f.get("value")
        comparator = f.get("comparator").upper()

        key = SearchUtils.translate_key_alias(key)

        if SearchUtils.is_string_attribute(
            type_, key, comparator
        ) or SearchUtils.is_numeric_attribute(type_, key, comparator):
            if key == "run_name":
                # Treat "attributes.run_name == <value>" as "tags.`mlflow.runName` == <value>".
                # The name column in the runs table is empty for runs logged in MLFlow <= 1.29.0.
                _filter &= _get_list_contains_query(
                    key=MLFLOW_RUN_NAME,
                    val=value,
                    comp=comparator,
                    list_field_name="tags",
                )
            else:
                key = MongoRun.get_attribute_name(key)
                _filter &= _get_filter_query(key, comparator, value)
        else:
            if SearchUtils.is_metric(type_, comparator):
                value = float(value)
                _filter &= _get_metrics_contains_query(
                    key=key, val=value, comp=comparator
                )
            elif SearchUtils.is_param(type_, comparator):
                entity = "params"
                _filter &= _get_list_contains_query(
                    key=key, val=value, comp=comparator, list_field_name=entity
                )
            elif SearchUtils.is_tag(type_, comparator):
                entity = "tags"
                _filter &= _get_list_contains_query(
                    key=key, val=value, comp=comparator, list_field_name=entity
                )
            else:
                raise MlflowException(
                    "Invalid search expression type '%s'" % type_,
                    error_code=INVALID_PARAMETER_VALUE,
                )

    return _filter


class MongoStore(AbstractStore):
    ARTIFACTS_FOLDER_NAME = "artifacts"

    DEFAULT_EXPERIMENT_ID = "0"

    filter_key = {
        ">": ["range", "must"],
        ">=": ["range", "must"],
        "=": ["term", "must"],
        "!=": ["term", "must_not"],
        "<=": ["range", "must"],
        "<": ["range", "must"],
        "LIKE": ["wildcard", "must"],
        "ILIKE": ["wildcard", "must"],
    }

    def __init__(self, store_uri: str, artifact_uri) -> None:
        super(MongoStore, self).__init__()

        self.is_plugin = True

        if artifact_uri is None:
            artifact_uri = DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH
        self.artifact_root_uri = resolve_uri_if_local(artifact_uri)

        parsed_uri = urllib.parse.urlparse(store_uri)
        params = dict(urllib.parse.parse_qsl(parsed_uri.query))

        self.__db_name = parsed_uri.path.replace("/", "")
        self.__conn = connect(
            db=self.__db_name,
            username=parsed_uri.username,
            password=parsed_uri.password,
            host=f"{parsed_uri.scheme}://{parsed_uri.netloc}",
            authentication_source=params.get("authSource", "admin"),
        )
        self.__db = get_db()

        if is_local_uri(artifact_uri):
            mkdir(local_file_uri_to_path(artifact_uri))

        if len(self.search_experiments(view_type=ViewType.ALL)) == 0:
            self._create_default_experiment()

    def create_experiment(self, name, artifact_location=None, tags=None):
        """
        Create a new experimen in backend store.

        :param name: Name of the experiment. This is expected to be unique in the backend store.
        :param artifact_location: Artifact location.
        :param tags: A list of :py:class:`MongoExperimentTag`
                     instances associated with this experiment
        :return: experiment_id (string) for the newly created experiment if successful, else None
        """

        _validate_experiment_name(name)

        if name in [obj.name for obj in MongoExperiment.objects.only("name")]:
            raise MlflowException(
                "Experiment(name={}) already exists.".format(name),
                RESOURCE_ALREADY_EXISTS,
            )

        if artifact_location:
            artifact_location = resolve_uri_if_local(artifact_location)

        creation_time = get_current_time_millis()

        tags_dict = {tag.key: tag.value for tag in tags} if tags else {}
        exp_tags = [
            MongoExperimentTag(key=key, value=value) for key, value in tags_dict.items()
        ]

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    mongo_experiment = MongoExperiment(
                        experiment_id=_get_next_exp_id(),
                        name=name,
                        lifecycle_stage=LifecycleStage.ACTIVE,
                        artifact_location=artifact_location,
                        tags=exp_tags,
                        creation_time=creation_time,
                        last_update_time=creation_time,
                    )
                    mongo_experiment.save()

                    if not artifact_location:
                        artifact_location = self._get_artifact_location(
                            mongo_experiment.id
                        )
                        mongo_experiment.update(artifact_location=artifact_location)
        except Exception as e:
            raise MlflowException(
                f"An error occurred during creating Experiment: {str(e)}"
            )

        return str(mongo_experiment.id)

    def _search_experiments(
        self, view_type, max_results, filter_string, order_by, page_token
    ):
        """
        Search for experiments in backend that satisfy the filter criteria.

        :param filter_string: A filter string expression. Currently supports a single filter
                              condition either name of model like ``name = 'experiment_name'`` etc.
        :param max_results: Maximum number of model versions desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_experiments`` call.
        :return: A Tuple of :py:class:`MongoExperiment`
                 objects that satisfy the search expressions. The pagination token for the next
                 page can be obtained via the ``token`` attribute of the object.
        """

        def compute_next_token(current_size):
            next_token = None
            if max_results + 1 == current_size:
                final_offset = offset + max_results
                next_token = SearchExperimentsUtils.create_page_token(final_offset)

            return next_token

        if not isinstance(max_results, int) or max_results < 1:
            raise MlflowException(
                "Invalid value for max_results. It must be a positive integer,"
                f" but got {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        if max_results > SEARCH_MAX_RESULTS_THRESHOLD:
            raise MlflowException(
                f"Invalid value for max_results. It must be at most {SEARCH_MAX_RESULTS_THRESHOLD},"
                f" but got {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        lifecycle_stages = set(LifecycleStage.view_type_to_stages(view_type))
        _filter = Q(**{"lifecycle_stage__in": lifecycle_stages})

        parsed_filters = SearchExperimentsUtils.parse_search_filter(filter_string)
        _filter &= _get_search_experiments_filter_clauses(parsed_filters)

        order_by_clauses = _get_search_experiments_order_by_clauses(order_by)
        offset = SearchUtils.parse_start_offset_from_page_token(page_token)

        mongo_experiments = MongoExperiment.objects(_filter).order_by(
            *order_by_clauses
        )[offset : max_results + offset + 1]

        next_page_token = compute_next_token(len(mongo_experiments))

        return mongo_experiments[:max_results], next_page_token

    def search_experiments(
        self,
        view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        filter_string=None,
        order_by=None,
        page_token=None,
    ):
        """
        Search for experiments in backend that satisfy the filter criteria.

        :param filter_string: A filter string expression. Currently supports a single filter
                              condition either name of model like ``name = 'experiment_name'`` etc.
        :param max_results: Maximum number of model versions desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_experiments`` call.
        :return: A PagedList of :py:class:`Experiment`
                 objects that satisfy the search expressions. The pagination token for the next
                 page can be obtained via the ``token`` attribute of the object.
        """
        mongo_experiments, next_page_token = self._search_experiments(
            view_type, max_results, filter_string, order_by, page_token
        )
        experiments = [e.to_mlflow_entity() for e in mongo_experiments]
        return PagedList(experiments, next_page_token)

    def _get_experiment(self, experiment_id: str) -> MongoExperiment:
        """
        Get experiment instance by experiment_id.

        :param experiment_id: experiment id.
        :return: A single :py:class:`MongoExperiment` object.
        """

        mongo_experiments = MongoExperiment.objects(experiment_id=experiment_id)

        if len(mongo_experiments) == 0:
            raise MlflowException(
                "Experiments with experiment_id={} not found".format(experiment_id),
                RESOURCE_DOES_NOT_EXIST,
            )
        if len(mongo_experiments) > 1:
            raise MlflowException(
                "Expected only 1 RegisteredModel with experiment_id={}. Found {}.".format(
                    experiment_id, len(mongo_experiments)
                ),
                INVALID_STATE,
            )

        return mongo_experiments[0]

    def get_experiment(self, experiment_id: str) -> Experiment:
        """
        Get experiment instance by experiment_id.

        :param experiment_id: experiment id.
        :return: A single :py:class:`Experiment` object.
        """
        return self._get_experiment(experiment_id).to_mlflow_entity()

    def _get_experiment_by_name(self, experiment_name: str) -> [MongoExperiment | None]:
        """
        Get experiment instance by experiment_name.

        :param experiment_name: experiment name.
        :return: A single :py:class:`MongoExperiment` object.
        """

        mongo_experiments = MongoExperiment.objects(name=experiment_name)

        if len(mongo_experiments) == 0:
            raise MlflowException(
                "Experiments with name={} not found".format(experiment_name),
                RESOURCE_DOES_NOT_EXIST,
            )
        if len(mongo_experiments) > 1:
            raise MlflowException(
                "Expected only 1 RegisteredModel with name={}. Found {}.".format(
                    experiment_name, len(mongo_experiments)
                ),
                INVALID_STATE,
            )

        return mongo_experiments[0]

    def get_experiment_by_name(self, experiment_name):
        """
        Get experiment instance by experiment_name.

        :param experiment_name: experiment name.
        :return: A single :py:class:`Experiment` object.
        """
        mongo_experiment = self._get_experiment_by_name(experiment_name)
        return (
            mongo_experiment.to_mlflow_entity()
            if mongo_experiment is not None
            else None
        )

    def delete_experiment(self, experiment_id):
        """
        Delete the experiment.
        Backend raises exception if an experiment with given id does not exist.

        :param experiment_id: experiment id.
        :return: None
        """
        mongo_experiment = self._get_experiment(experiment_id)
        mongo_runs = MongoRun.objects(experiment_id=experiment_id)

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    mongo_experiment.update(
                        lifecycle_stage=LifecycleStage.DELETED,
                        last_update_time=get_current_time_millis(),
                    )
                    for mongo_run in mongo_runs:
                        mongo_run.update(
                            lifecycle_stage=LifecycleStage.DELETED,
                            deleted_time=get_current_time_millis(),
                        )
        except Exception as e:
            raise MlflowException(
                f"Experimentx deleting error (experiment_id={experiment_id}): {str(e)}"
            )

    def restore_experiment(self, experiment_id):
        """
        Restore the experiment.
        Backend raises exception if an experiment with given id does not exist.

        :param experiment_id: experiment id.
        :return: None
        """

        mongo_experiment = self._get_experiment(experiment_id)
        mongo_runs = MongoRun.objects(experiment_id=experiment_id)

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    mongo_experiment.update(
                        lifecycle_stage=LifecycleStage.ACTIVE,
                        last_update_time=get_current_time_millis(),
                    )
                    for mongo_run in mongo_runs:
                        mongo_run.update(
                            lifecycle_stage=LifecycleStage.ACTIVE, deleted_time=None
                        )
        except Exception as e:
            raise MlflowException(
                f"Experiment restoring error (experiment_id={experiment_id}): {str(e)}"
            )

    def rename_experiment(self, experiment_id: str, new_name: str) -> None:
        """
        Rename the experiment.

        :param experiment_id: experiment id.
        :param new_name: New proposed name.
        :return: None
        """
        mongo_experiment = self._get_experiment(experiment_id)
        if mongo_experiment.lifecycle_stage != LifecycleStage.ACTIVE:
            raise MlflowException(
                "Cannot rename a non-active experiment.", INVALID_STATE
            )
        mongo_experiment.update(
            name=new_name, last_update_time=get_current_time_millis()
        )

    def _check_experiment_is_active(self, experiment: MongoExperiment) -> None:
        if experiment.lifecycle_stage != LifecycleStage.ACTIVE:
            raise MlflowException(
                "The experiment {} must be in the 'active' state. "
                "Current state is {}.".format(
                    experiment.id, experiment.lifecycle_stage
                ),
                INVALID_PARAMETER_VALUE,
            )

    def create_run(self, experiment_id, user_id, start_time, tags, run_name) -> Run:
        """
        Create a new run in backend store.

        :param experiment_id: experiment id.
        :param user_id: user id.
        :param start_time: start_time
        :param tags: A list of :py:class:`MongoTag`
                     instances associated with this run
        :param run_name: run name.
        :return: RUN
        """
        mongo_experiment = self._get_experiment(experiment_id)
        self._check_experiment_is_active(mongo_experiment)

        run_id = uuid.uuid4().hex
        artifact_location = append_to_uri_path(
            mongo_experiment.artifact_location, run_id, MongoStore.ARTIFACTS_FOLDER_NAME
        )

        tags = tags or []
        run_name_tag = _get_run_name_from_tags(tags)
        if run_name and run_name_tag and (run_name != run_name_tag):
            raise MlflowException(
                "Both 'run_name' argument and 'mlflow.runName' tag are specified, but with "
                f"different values (run_name='{run_name}', mlflow.runName='{run_name_tag}').",
                INVALID_PARAMETER_VALUE,
            )

        run_name = run_name or run_name_tag or _generate_random_name()
        if not run_name_tag:
            tags.append(RunTag(key=MLFLOW_RUN_NAME, value=run_name))

        run_tags = [MongoTag(key=tag.key, value=tag.value) for tag in tags]
        mongo_run = MongoRun(
            run_name=run_name,
            artifact_uri=artifact_location,
            run_uuid=run_id,
            experiment_id=experiment_id,
            source_type=SourceType.to_string(SourceType.UNKNOWN),
            source_name="",
            entry_point_name="",
            user_id=user_id,
            status=RunStatus.to_string(RunStatus.RUNNING),
            start_time=start_time,
            end_time=None,
            deleted_time=None,
            source_version="",
            lifecycle_stage=LifecycleStage.ACTIVE,
            tags=run_tags,
        )

        mongo_run.save()
        return mongo_run.to_mlflow_entity()

    def _get_run(self, run_uuid: str) -> MongoRun:
        """
        Get run instance by run_uuid.

        :param run_uuid: run uuid.
        :return: A single :py:class:`MongoRun` object.
        """
        mongo_runs = MongoRun.objects(run_uuid=run_uuid)

        if len(mongo_runs) == 0:
            raise MlflowException(
                "Run with id={} not found".format(run_uuid), RESOURCE_DOES_NOT_EXIST
            )
        if len(mongo_runs) > 1:
            raise MlflowException(
                "Expected only 1 run with id={}. Found {}.".format(
                    run_uuid, len(mongo_runs)
                ),
                INVALID_STATE,
            )

        return mongo_runs[0]

    def get_run(self, run_id):
        """
        Get run instance by run_id.

        :param run_id: run id.
        :return: A single :py:class:`Run` object.
        """
        return self._get_run(run_id).to_mlflow_entity()

    def _check_run_is_active(self, run: MongoRun) -> None:
        if run.lifecycle_stage != LifecycleStage.ACTIVE:
            raise MlflowException(
                "The run {} must be in the 'active' state. Current state is {}.".format(
                    run.id, run.lifecycle_stage
                ),
                INVALID_PARAMETER_VALUE,
            )

    def update_run_info(self, run_id, run_status, end_time, run_name):

        """
        Update the information of an existing run in the backend store.

        :param run_id: The unique identifier for the run.
        :param run_status: The status of the run.
        :param end_time: The time the run ended.
        :param run_name: The new name of the run. If not provided, the original name is kept.
        :return: The updated run information.
        """

        mongo_run = self._get_run(run_id)
        self._check_run_is_active(mongo_run)

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    mongo_run.update(
                        status=RunStatus.to_string(run_status), end_time=end_time
                    )
                    if run_name:
                        mongo_run.update(run_name=run_name)
                        num_updates = mongo_run.tags.filter(key=MLFLOW_RUN_NAME).update(
                            key=MLFLOW_RUN_NAME, value=run_name
                        )
                        if num_updates == 0:
                            mongo_run.tags.append(
                                MongoTag(key=MLFLOW_RUN_NAME, value=run_name)
                            )
                        mongo_run.save()

                    mongo_run.reload()
                    return mongo_run.to_mlflow_entity().info
        except Exception as e:
            raise MlflowException(f"Run update error (run_id={run_id}): {str(e)}")

    def restore_run(self, run_id):
        """
        Restore the run.
        Backend raises exception if an experiment with given id does not exist.

        :param run_id: run id.
        :return: None
        """
        mongo_run = self._get_run(run_id)
        mongo_run.update(lifecycle_stage=LifecycleStage.ACTIVE, deleted_time=None)

    def delete_run(self, run_id):
        """
        Delete the run.
        Backend raises exception if an experiment with given id does not exist.

        :param run_id: run id.
        :return: None
        """
        mongo_run = self._get_run(run_id)
        mongo_run.update(
            lifecycle_stage=LifecycleStage.DELETED,
            deleted_time=get_current_time_millis(),
        )

    def _hard_delete_run(self, run_id):
        """
        Hard delete the run.
        Backend raises exception if an experiment with given id does not exist.

        :param run_id: run id.
        :return: None
        """
        MongoRun.objects(run_uuid=run_id).delete()

    def _get_deleted_runs(self, older_than=0):
        """
        get deleted runs.

        :param older_than: oolder_than.
        :return: List[str]
        """
        current_time = get_current_time_millis()
        return [
            r.run_uuid
            for r in MongoRun.objects(
                lifecycle_stage=LifecycleStage.DELETED,
                deleted_time__lte=(current_time - older_than),
            )
        ]

    def _get_metric_value_details(self, metric):
        """
        Validates and processes a given metric.

        :param metric: A metric instance to validate and process.
        :return: Tuple of (metric, value, is_nan).
        """
        _validate_metric(metric.key, metric.value, metric.timestamp, metric.step)
        is_nan = math.isnan(metric.value)
        if is_nan:
            value = 0
        elif math.isinf(metric.value):
            #  NB: Sql can not represent Infs = > We replace +/- Inf with max/min 64b float value
            value = (
                1.7976931348623157e308 if metric.value > 0 else -1.7976931348623157e308
            )
        else:
            value = metric.value
        return metric, value, is_nan

    def _log_metrics(self, run, metrics):
        """
        Logs a list of metrics for a given run.

        :param run: The run for which the metrics are being logged.
        :param metrics: A list of metrics to log.
        :return: None
        """
        mongo_metric_instances = []
        seen = set()
        for metric in metrics:
            metric, value, is_nan = self._get_metric_value_details(metric)
            if metric not in seen:
                mongo_metric_instances.append(
                    MongoMetric(
                        run_id=run.id,
                        key=metric.key,
                        value=value,
                        timestamp=metric.timestamp,
                        step=metric.step,
                        is_nan=is_nan,
                    )
                )
                seen.add(metric)

        def _insert_metrics(metric_instances):
            MongoMetric.objects.insert(metric_instances, load_bulk=False)
            for m in metric_instances:
                self._update_latest_metric_if_necessary(run, m)

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    _insert_metrics(mongo_metric_instances)
        except BulkWriteError:
            pass

    def _update_latest_metric_if_necessary(self, run, logged_metric):
        """
        Update the latest metric of a run if the logged metric is more recent.

        :param run: The run whose latest metric might need to be updated.
        :param logged_metric: The newly logged metric.
        :return: None
        """

        def _compare_metrics(metric_a, metric_b):
            """
            :return: True if ``metric_a`` is strictly more recent than ``metric_b``, as determined
                     by ``step``, ``timestamp``, and ``value``. False otherwise.
            """
            return (metric_a.step, metric_a.timestamp, metric_a.value) > (
                metric_b.step,
                metric_b.timestamp,
                metric_b.value,
            )

        mongo_new_latest_metric = MongoLatestMetric(
            key=logged_metric.key,
            value=logged_metric.value,
            timestamp=logged_metric.timestamp,
            step=logged_metric.step,
            is_nan=logged_metric.is_nan,
        )

        latest_metric_exist = False
        for i, latest_metric in enumerate(run.latest_metrics):
            if latest_metric.key == logged_metric.key:
                latest_metric_exist = True
                if _compare_metrics(mongo_new_latest_metric, latest_metric):
                    run.latest_metrics[i] = mongo_new_latest_metric
        if not latest_metric_exist:
            run.update(push__latest_metrics=mongo_new_latest_metric)

    def get_metric_history(self, run_id, metric_key, max_results=None, page_token=None):
        """
        Return all logged values for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run
        :param max_results: An indicator for paginated results. This functionality is not
            implemented for SQLAlchemyStore and is unused in this store's implementation.
        :param page_token: An indicator for paginated results. This functionality is not
            implemented for SQLAlchemyStore and if the value is overridden with a value other than
            ``None``, an MlflowException will be thrown.

        :return: A List of :py:class:`mlflow.entities.Metric` entities if ``metric_key`` values
            have been logged to the ``run_id``, else an empty list.
        """
        if page_token is not None:
            raise MlflowException(
                "The SQLAlchemyStore backend does not support pagination for the "
                f"`get_metric_history` API. Supplied argument `page_token` '{page_token}' must be "
                "`None`."
            )

        mongo_metrics = MongoMetric.objects(run_id=run_id, key=metric_key)
        return PagedList([m.to_mlflow_entity() for m in mongo_metrics], None)

    def log_param(self, run_id, param):
        """
        Log param.

        :param run_id: run id.
        :param param: :py:class:MongoParam` instance to log.
        :return: None
        """

        _validate_param(param.key, param.value)

        mongo_run = self._get_run(run_uuid=run_id)
        self._check_run_is_active(mongo_run)

        self._log_param(mongo_run, param)

    def _log_param(self, mongo_run, param):
        """
        Log param.

        :param mongo_run: Run.
        :param param: :py:class:MongoParam` instance to log.
        :return: None
        """

        existing_param = mongo_run.get_param_by_key(param.key)
        if existing_param:
            if existing_param.value != param.value:
                raise MlflowException(
                    "Changing param values is not allowed. Params were already"
                    f" logged='{param}' for run ID='{mongo_run.id}'.",
                    INVALID_PARAMETER_VALUE,
                )
            else:
                return
        new_param = MongoParam(key=param.key, value=param.value)
        mongo_run.update(push__params=new_param)
        mongo_run.reload()

    def set_experiment_tag(self, experiment_id, tag):
        """
        Set a tag for the experiment.

        :param experiment_id: experiment id.
        :param tag: :py:class:EexperimentTag` instance to log.
        :return: None
        """
        _validate_experiment_tag(tag.key, tag.value)
        mongo_experiment = self._get_experiment(experiment_id)
        self._check_experiment_is_active(mongo_experiment)
        mongo_experiment.update(
            push__tags=MongoExperimentTag(key=tag.key, value=tag.value)
        )

    def set_tag(self, run_id, tag):
        """
        Set a tag on a run.

        :param run_id: String ID of the run
        :param tag: RunTag instance to log
        """
        _validate_tag(tag.key, tag.value)

        mongo_run = self._get_run(run_uuid=run_id)

        self._check_run_is_active(mongo_run)

        self._set_tag(mongo_run, tag)

    def _set_tag(self, mongo_run, tag):
        """
        Set a tag for the registered model.

        :param mongo_run: Mongo Run.
        :param tag: :py:class:`MongoTag` instance to log.
        :return: None
        """
        if tag.key == MLFLOW_RUN_NAME:
            mongo_run.update(name=tag.value)

        existing = mongo_run.tags.filter(key=tag.key)
        if existing.count() == 0:
            new_tag = MongoTag(key=tag.key, value=tag.value)
            mongo_run.update(push__tags=new_tag)
        else:
            existing.update(key=tag.key, value=tag.value)
            mongo_run.save()

    def delete_tag(self, run_id, key):
        """
        Delete a tag associated with the run.

        :param run_id: run id.
        :param key: run tag key.
        :return: None
        """
        mongo_run = self._get_run(run_id)
        self._check_run_is_active(mongo_run)
        tags = mongo_run.get_tags_by_key(key)
        if len(tags) == 0:
            raise MlflowException(
                f"No tag with name: {key} in run with id {mongo_run.id}",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )
        elif len(tags) > 1:
            raise MlflowException(
                "Bad data in database - tags for a specific run must have "
                "a single unique value. "
                "See https://mlflow.org/docs/latest/tracking.html#adding-tags-to-runs",
                error_code=INVALID_STATE,
            )
        mongo_run.update(pull__tags=tags[0])

    def _search_runs(
        self,
        experiment_ids,
        filter_string,
        run_view_type,
        max_results,
        order_by,
        page_token,
    ):
        """
        Search for runs in the given experiment_ids with the filter_string, run_view_type, max_results, order_by, and page_token.

        :param experiment_ids: A list of ids of the experiments to search within.
        :param filter_string: A string to filter the runs.
        :param run_view_type: A RunViewType value describing which type of runs should be returned.
        :param max_results: The maximum number of runs to return.
        :param order_by: A list of order_by clauses.
        :param page_token: A token representing the page to retrieve.
        :return: A list of runs and the next page token.
        """

        experiment_ids = list(experiment_ids)
        if max_results > SEARCH_MAX_RESULTS_THRESHOLD:
            raise MlflowException(
                "Invalid value for request parameter max_results. It must be at "
                f"most {SEARCH_MAX_RESULTS_THRESHOLD}, but got value {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        lifecycle_stages = list(set(LifecycleStage.view_type_to_stages(run_view_type)))
        _filter = Q(experiment_id__in=experiment_ids)
        _filter &= Q(lifecycle_stage__in=lifecycle_stages)

        parsed_filters = SearchUtils.parse_search_filter(filter_string)
        _filter &= _get_search_run_filter_clauses(parsed_filters)

        mongo_runs = MongoRun.objects(_filter)
        runs = [r.to_mlflow_entity() for r in mongo_runs]
        runs = SearchUtils.sort(runs, order_by)
        runs, next_page_token = SearchUtils.paginate(runs, page_token, max_results)

        return runs, next_page_token

    def log_batch(
        self,
        run_id: str,
        metrics: List[Metric],
        params: List[Param],
        tags: List[RunTag],
    ) -> None:
        """
        Log a batch of metrics, parameters, and tags for a given run.

        :param run_id: The unique identifier for the run.
        :param metrics: A list of Metric instances to be logged.
        :param params: A list of Param instances to be logged.
        :param tags: A list of RunTag instances to be logged.
        :return: None
        """
        _validate_run_id(run_id)
        _validate_batch_log_data(metrics, params, tags)
        _validate_batch_log_limits(metrics, params, tags)
        _validate_param_keys_unique(params)

        mongo_run = self._get_run(run_uuid=run_id)
        self._check_run_is_active(mongo_run)
        try:
            if metrics:
                self._log_metrics(mongo_run, metrics)
            for param in params:
                self._log_param(mongo_run, param)
            for tag in tags:
                self._set_tag(mongo_run, tag)
            mongo_run.save()
        except MlflowException as e:
            raise e
        except Exception as e:
            raise MlflowException(e)

    def record_logged_model(self, run_id, mlflow_model):
        """
        Record a logged model for a given run.

        :param run_id: The unique identifier for the run.
        :param mlflow_model: An instance of mlflow.models.Model that represents the model to be logged.
        :return: None
        """
        model_dict = mlflow_model.to_dict()
        mongo_run = self._get_run(run_uuid=run_id)
        self._check_run_is_active(mongo_run)
        previous_tag = [t for t in mongo_run.tags if t.key == MLFLOW_LOGGED_MODELS]
        if previous_tag:
            value = json.dumps(json.loads(previous_tag[0].value) + [model_dict])
        else:
            value = json.dumps([model_dict])
        _validate_tag(MLFLOW_LOGGED_MODELS, value)
        self._set_tag(mongo_run, RunTag(key=MLFLOW_LOGGED_MODELS, value=value))

    def _create_default_experiment(self):
        """
        MLflow UI and client code expects a default experiment with ID 0.
        This method uses SQL insert statement to create the default experiment as a hack, since
        experiment table uses 'experiment_id' column is a PK and is also set to auto increment.
        MySQL and other implementation do not allow value '0' for such cases.

        ToDo: Identify a less hacky mechanism to create default experiment 0
        """
        SequenceId.drop_collection()
        creation_time = get_current_time_millis()
        mongo_experiment = MongoExperiment(
            experiment_id=_get_next_exp_id(start_over=True),
            name=Experiment.DEFAULT_EXPERIMENT_NAME,
            artifact_location=self._get_artifact_location(0),
            lifecycle_stage=LifecycleStage.ACTIVE,
            creation_time=creation_time,
            last_update_time=creation_time,
        )
        mongo_experiment.save()

    def _get_artifact_location(self, experiment_id):
        """
        Get artifact location.
        :param experiment_id: experiment id.
        :return: artifact location :str
        """
        return append_to_uri_path(self.artifact_root_uri, str(experiment_id))
