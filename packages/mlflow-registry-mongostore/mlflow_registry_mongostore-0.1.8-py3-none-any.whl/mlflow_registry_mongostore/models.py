import numbers
from datetime import datetime
from flask import request
from mlflow.entities.model_registry import (
    RegisteredModel,
    ModelVersion,
    RegisteredModelTag,
    ModelVersionTag,
)
from mlflow.entities.model_registry.model_version_stages import STAGE_NONE
from mlflow.utils.time_utils import get_current_time_millis
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus
from mongoengine import (
    Document,
    StringField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    LongField,
    ReferenceField,
    CASCADE,
    QuerySet,
    Q,
    DateTimeField,
)


REGISTERED_MODEL_COLLECTION_NAME = "mlflow_registered_model"
MODEL_VERSION_COLLECTION_NAME = "mlflow_model_version"


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


class MongoRegisteredModelTag(EmbeddedDocument):
    key = StringField(required=True, max_length=250)
    value = StringField(required=True, max_length=5000)

    def to_mlflow_entity(self) -> RegisteredModelTag:
        return RegisteredModelTag(
            key=self.key,
            value=self.value,
        )


class MongoModelVersionTag(EmbeddedDocument):
    key = StringField(required=True, max_length=250)
    value = StringField(required=True, max_length=5000)

    def to_mlflow_entity(self) -> ModelVersionTag:
        return ModelVersionTag(
            key=self.key,
            value=self.value,
        )


class MongoRegisteredModel(Document):
    name = StringField(primary_key=True)
    registed_model_id = StringField(max_length=32, db_field="id")
    creation_timestamp = LongField(default=get_current_time_millis)
    last_updated_timestamp = LongField()
    description = StringField(max_length=256)
    tags = ListField(EmbeddedDocumentField(MongoRegisteredModelTag))
    mlflow_workspace_id = StringField(max_length=36)
    _created_at = DateTimeField(default=datetime.utcnow)
    _updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": REGISTERED_MODEL_COLLECTION_NAME,
        "queryset_class": CustomQuerySet,
    }

    def to_mlflow_entity(self) -> RegisteredModel:
        return RegisteredModel(
            name=self.name,
            creation_timestamp=self.creation_timestamp,
            last_updated_timestamp=self.last_updated_timestamp,
            description=self.description,
            tags=[t.to_mlflow_entity() for t in self.tags],
        )

    def get_tags_by_key(self, key):
        return list(filter(lambda param: param.key == key, self.tags))

    def save(self, *args, **kwargs):
        if not self.id:
            self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self.mlflow_workspace_id = get_workspace_id()
        self.registed_model_id = self.name
        return super(MongoRegisteredModel, self).save(*args, **kwargs)


class MongoModelVersion(Document):
    # name = StringField(primary_key=True)
    registered_model_id = ReferenceField(
        "MongoRegisteredModel",
        reverse_delete_rule=CASCADE,
        db_field="mlflow_registered_model_id",
    )
    version = IntField(required=True)
    creation_timestamp = LongField(default=get_current_time_millis)
    last_updated_timestamp = LongField()
    description = StringField(max_length=5000)
    user_id = StringField(max_length=256)
    current_stage = StringField(max_length=20, default=STAGE_NONE)
    source = StringField(max_length=200)
    run_id = StringField(max_length=32, db_field="mlflow_run_id")
    run_link = StringField(max_length=500)
    status = StringField(
        max_length=20, default=ModelVersionStatus.to_string(ModelVersionStatus.READY)
    )
    status_message = StringField(max_length=500)
    mlflow_workspace_id = StringField(max_length=36)
    _created_at = DateTimeField(default=datetime.utcnow)
    _updated_at = DateTimeField(default=datetime.utcnow)

    tags = ListField(EmbeddedDocumentField(MongoModelVersionTag))

    meta = {
        "collection": MODEL_VERSION_COLLECTION_NAME,
        "queryset_class": CustomQuerySet,
    }

    def to_mlflow_entity(self) -> ModelVersion:
        return ModelVersion(
            name=str(self.registered_model_id.id),
            version=self.version,
            creation_timestamp=self.creation_timestamp,
            last_updated_timestamp=self.last_updated_timestamp,
            description=self.description,
            user_id=self.user_id,
            current_stage=self.current_stage,
            source=self.source,
            run_id=self.run_id,
            run_link=self.run_link,
            status=self.status,
            status_message=self.status_message,
            tags=[t.to_mlflow_entity() for t in self.tags],
        )

    def get_tags_by_key(self, key):
        return list(filter(lambda param: param.key == key, self.tags))

    @staticmethod
    def get_attribute_name(mlflow_attribute_name):
        return {"name": "registered_model_id"}.get(
            mlflow_attribute_name, mlflow_attribute_name
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        self.mlflow_workspace_id = get_workspace_id()
        return super(MongoModelVersion, self).save(*args, **kwargs)
