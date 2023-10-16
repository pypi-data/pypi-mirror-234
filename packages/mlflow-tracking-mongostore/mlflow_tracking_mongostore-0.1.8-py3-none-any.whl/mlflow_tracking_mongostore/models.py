import numbers
from datetime import datetime
from flask import request
from mlflow.entities import (
    Experiment,
    ExperimentTag,
    RunTag,
    RunInfo,
    RunData,
    Run,
    Metric,
    Param,
    SourceType,
    RunStatus,
)
from mlflow.entities import LifecycleStage
from mlflow.utils.mlflow_tags import _get_run_name_from_tags
from mlflow.utils.time_utils import get_current_time_millis
from mongoengine import (
    Document,
    StringField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    BooleanField,
    LongField,
    ReferenceField,
    CASCADE,
    EmbeddedDocumentListField,
    QuerySet,
    Q,
    DateTimeField,
)


EXPERIMENT_COLLECTION_NAME = "mlflow_experiment"
RUN_COLLECTION_NAME = "mlflow_run"
METRIC_COLLECTION_NAME = "mlflow_metric"


def get_workspace_id():
    if request:
        if request.headers:
            if "Workspace-Id" in request.headers:
                return request.headers["Workspace-Id"]
    return None


class CustomQuerySet(QuerySet):
    def __call__(self, q_obj=None, **query):

        q_obj = q_obj if q_obj else Q()

        # Combine the existing query with the new filter
        workspace_id = get_workspace_id()
        if workspace_id is not None:
            q_obj &= Q(mlflow_workspace_id__exists=True, mlflow_workspace_id__ne="")
            q_obj &= Q(mlflow_workspace_id=workspace_id)

        # call the super class's __call__ with the updated query.
        return super().__call__(q_obj, **query)


def compare_attr(val1, comp, val2):
    """
    Compares two values based on a comparator and returns the result.

    :param val1: The first value to be compared.
    :param comp: The comparator string. Can be one of [">", ">=", "!=", "=", "<", "<=", "LIKE", "ILIKE
    """
    if type(val1) != type(val2):
        return False

    is_numeric = isinstance(val1, numbers.Number)
    if is_numeric:
        if comp == ">":
            return val1 > val2
        elif comp == ">=":
            return val1 > val2
        elif comp == "!=":
            return val1 > val2
        elif comp == "=":
            return val1 > val2
        elif comp == "<":
            return val1 > val2
        elif comp == "<=":
            return val1 > val2
        return False
    else:
        if comp == "=":
            return val1 == val2
        elif comp == "!=":
            return val1 == val2
        elif comp == "LIKE":
            return val1.contains(val2)
        elif comp == "ILIKE":
            return val1.lower().contains(val2.lower())


def _get_next_exp_id(start_over=False):
    """
    Returns the next experiment ID based on the current sequence. If `start_over` is True, the sequence is reset and the ID "0" is returned.

    :param start_over: A boolean indicating if the sequence should be reset. Defaults to False.
    :return: A string representing the next experiment ID in the sequence.
    """
    if start_over:
        seq = SequenceId(collection_name=EXPERIMENT_COLLECTION_NAME, sequence_value=0)
        seq.save()
        return "0"

    return str(
        SequenceId._get_collection().find_one_and_update(
            filter={"_id": EXPERIMENT_COLLECTION_NAME},
            update={"$inc": {"sequence_value": 1}},
            new=True,
        )["sequence_value"]
    )


class SequenceId(Document):
    collection_name = StringField(primary_key=True)
    sequence_value = LongField()


class MongoExperimentTag(EmbeddedDocument):
    key = StringField(required=True)
    value = StringField(required=True)

    def to_mlflow_entity(self) -> ExperimentTag:
        return ExperimentTag(key=self.key, value=self.value)


class MongoExperiment(Document):
    experiment_id = StringField(primary_key=True)
    exp_id = StringField(max_length=32, db_field="id")
    name = StringField(required=True, max_length=200)
    artifact_location = StringField(max_length=256)
    lifecycle_stage = StringField(
        max_length=50, default=LifecycleStage.ACTIVE, db_field="_lifecycle_stage"
    )
    tags = ListField(EmbeddedDocumentField(MongoExperimentTag))
    creation_time = LongField()
    last_update_time = LongField()
    mlflow_workspace_id = StringField(max_length=36)
    _created_at = DateTimeField(default=datetime.utcnow)
    _updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": EXPERIMENT_COLLECTION_NAME,
        "strict": False,
        "queryset_class": CustomQuerySet,
    }

    def to_mlflow_entity(self) -> Experiment:
        return Experiment(
            experiment_id=str(self.id),
            name=self.name,
            artifact_location=self.artifact_location,
            lifecycle_stage=self.lifecycle_stage,
            tags=[t.to_mlflow_entity() for t in self.tags],
            creation_time=self.creation_time,
            last_update_time=self.last_update_time,
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self.mlflow_workspace_id = get_workspace_id()
        self.exp_id = self.experiment_id
        return super(MongoExperiment, self).save(*args, **kwargs)


class MongoTag(EmbeddedDocument):
    key = StringField(required=True)
    value = StringField(required=True)

    def to_mlflow_entity(self) -> RunTag:
        return RunTag(key=self.key, value=self.value)


class MongoParam(EmbeddedDocument):
    key = StringField(required=True)
    value = StringField(required=True)

    def to_mlflow_entity(self) -> Param:
        return Param(key=self.key, value=self.value)


class MongoMetric(Document):
    key = StringField(required=True)
    timestamp = LongField(default=get_current_time_millis)
    step = LongField(required=True, default=0)
    is_nan = BooleanField(required=True, default=False)
    run_id = StringField(required=True, db_field="mlflow_run_id")
    value = FloatField(
        unique_with=["key", "timestamp", "step", "run_id"], required=True
    )

    meta = {"collection": METRIC_COLLECTION_NAME}

    def to_mlflow_entity(self) -> Metric:
        return Metric(
            key=self.key,
            value=self.value if not self.is_nan else float("nan"),
            timestamp=self.timestamp,
            step=self.step,
        )


class MongoLatestMetric(EmbeddedDocument):
    key = StringField()
    value = FloatField()
    timestamp = LongField()
    step = IntField()
    is_nan = BooleanField()

    def to_mlflow_entity(self) -> Metric:
        return Metric(
            key=self.key,
            value=self.value if not self.is_nan else float("nan"),
            timestamp=self.timestamp,
            step=self.step,
        )


class MongoRun(Document):
    run_uuid = StringField(primary_key=True, required=True, max_length=32)
    run_id = StringField(max_length=32, db_field="id")
    run_name = StringField(max_length=250)
    source_type = StringField(
        max_length=20, default=SourceType.to_string(SourceType.LOCAL)
    )
    source_name = StringField(max_length=500)
    entry_point_name = StringField(max_length=50)
    user_id = StringField(max_length=256, default="")
    status = StringField(
        max_length=20, default=RunStatus.to_string(RunStatus.SCHEDULED)
    )
    start_time = LongField(default=get_current_time_millis)
    end_time = LongField()
    deleted_time = LongField()
    source_version = StringField(max_length=50)
    lifecycle_stage = StringField(
        max_length=20, default=LifecycleStage.ACTIVE, db_field="_lifecycle_stage"
    )
    artifact_uri = StringField(max_length=200)

    experiment_id = ReferenceField(
        "MongoExperiment", reverse_delete_rule=CASCADE, db_field="mlflow_experiment_id"
    )
    mlflow_workspace_id = StringField(max_length=36)
    _created_at = DateTimeField(default=datetime.utcnow)
    _updated_at = DateTimeField(default=datetime.utcnow)

    latest_metrics = ListField(EmbeddedDocumentField(MongoLatestMetric))
    params = ListField(EmbeddedDocumentField(MongoParam))
    # tags = ListField(EmbeddedDocumentField(MongoTag))
    tags = EmbeddedDocumentListField(MongoTag)

    meta = {"collection": RUN_COLLECTION_NAME, "queryset_class": CustomQuerySet}

    def to_mlflow_entity(self) -> Run:
        run_info = RunInfo(
            run_uuid=self.run_uuid,
            run_id=self.run_uuid,
            run_name=self.run_name,
            experiment_id=str(self.experiment_id.id),
            user_id=self.user_id,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            lifecycle_stage=self.lifecycle_stage,
            artifact_uri=self.artifact_uri,
        )

        tags = [t.to_mlflow_entity() for t in self.tags]
        run_data = RunData(
            metrics=[m.to_mlflow_entity() for m in self.latest_metrics],
            params=[p.to_mlflow_entity() for p in self.params],
            tags=tags,
        )

        if not run_info.run_name:
            run_name = _get_run_name_from_tags(tags)
            if run_name:
                run_info._set_run_name(run_name)

        return Run(run_info=run_info, run_data=run_data)

    @staticmethod
    def get_attribute_name(mlflow_attribute_name):
        return {"run_id": "run_uuid"}.get(mlflow_attribute_name, mlflow_attribute_name)

    @property
    def metrics(self):
        return MongoMetric.objects(run_uuid=self.run_uuid)

    def get_param_by_key(self, key):
        params = list(filter(lambda param: param.key == key, self.params))
        return params[0] if params else None

    def get_tags_by_key(self, key):
        return list(filter(lambda param: param.key == key, self.tags))

    def save(self, *args, **kwargs):
        if not self.id:
            self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self.mlflow_workspace_id = get_workspace_id()
        self.run_id = self.run_uuid
        return super(MongoRun, self).save(*args, **kwargs)
