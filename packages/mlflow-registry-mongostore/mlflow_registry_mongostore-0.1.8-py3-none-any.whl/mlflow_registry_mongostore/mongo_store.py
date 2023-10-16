from __future__ import annotations
from mongoengine.connection import get_db
from mongoengine.errors import NotUniqueError
from mlflow.entities.model_registry.model_version_stages import (
    get_canonical_stage,
    ALL_STAGES,
    STAGE_DELETED_INTERNAL,
    DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS,
    STAGE_ARCHIVED,
)
from mlflow.utils.search_utils import (
    SearchUtils,
    SearchModelUtils,
    SearchModelVersionUtils,
)
from mlflow.protos.databricks_pb2 import (
    INVALID_PARAMETER_VALUE,
    RESOURCE_ALREADY_EXISTS,
    INVALID_STATE,
    RESOURCE_DOES_NOT_EXIST,
)
from mlflow.store.model_registry import (
    SEARCH_REGISTERED_MODEL_MAX_RESULTS_DEFAULT,
    SEARCH_REGISTERED_MODEL_MAX_RESULTS_THRESHOLD,
    SEARCH_MODEL_VERSION_MAX_RESULTS_DEFAULT,
    SEARCH_MODEL_VERSION_MAX_RESULTS_THRESHOLD,
)
from mlflow.utils.validation import (
    _validate_registered_model_tag,
    _validate_model_version_tag,
    _validate_model_name,
    _validate_model_version,
    _validate_tag_name,
)
from mlflow.store.entities import PagedList
from mlflow.store.model_registry.abstract_store import AbstractStore
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from six.moves import urllib
from mlflow.exceptions import MlflowException
from mlflow.utils.time_utils import get_current_time_millis
from .models import (
    MongoRegisteredModel,
    MongoModelVersion,
    MongoModelVersionTag,
    MongoRegisteredModelTag,
)


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


def _get_search_registered_model_filter_clauses(parsed_filters):
    """
    Constructs a MongoDB filter query based on provided filters for searching registered models.

    :param parsed_filters: A list of filter conditions parsed from search query. Each filter condition is a dictionary
                           that contains 'type', 'key', 'comparator', and 'value'.
                           For example, a filter condition can be {"type": "attribute", "key": "name", "comparator": "=", "value": "model1"}.
    :raises MlflowException: If the comparator for string or numeric attribute is invalid,
                             or if the comparator for tag is invalid, or if the token type is invalid.
    :return: A Q object representing the filter query for MongoDB.
    """
    _filter = Q()
    for f in parsed_filters:
        type_ = f["type"]
        key = f["key"]
        comparator = f["comparator"]
        value = f["value"]
        if type_ == "attribute":
            if SearchUtils.is_string_attribute(
                type_, key, comparator
            ) and comparator not in ("=", "!=", "LIKE", "ILIKE"):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for string attribute: {comparator}"
                )
            if SearchUtils.is_numeric_attribute(
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


def _get_search_model_version_filter_clauses(parsed_filters):
    """
    Constructs a MongoDB filter query based on provided filters for searching model versions.

    :param parsed_filters: A list of filter conditions parsed from search query. Each filter condition is a dictionary
                           that contains 'type', 'key', 'comparator', and 'value'.
                           For example, a filter condition can be {"type": "attribute", "key": "name", "comparator": "=", "value": "version1"}.
    :raises MlflowException: If the comparator for string or numeric attribute is invalid,
                             or if the comparator for tag is invalid, or if the token type is invalid.
    :return: A Q object representing the filter query for MongoDB.
    """
    _filter = Q()
    for f in parsed_filters:
        type_ = f["type"]
        key = f["key"]
        comparator = f["comparator"]
        value = f["value"]
        if type_ == "attribute":
            if SearchUtils.is_string_attribute(
                type_, key, comparator
            ) and comparator not in ("=", "!=", "LIKE", "ILIKE"):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for string attribute: {comparator}"
                )
            if SearchUtils.is_numeric_attribute(
                type_, key, comparator
            ) and comparator not in ("=", "!=", "<", "<=", ">", ">="):
                raise MlflowException.invalid_parameter_value(
                    f"Invalid comparator for numeric attribute: {comparator}"
                )
            key = MongoModelVersion.get_attribute_name(key)
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


def _get_search_model_version_order_by_clauses(order_by):
    """
    Constructs a list of sorting directives based on the provided ordering instructions.

    :param order_by: A list of strings specifying the ordering of the returned model versions.
                     Each string is a space-separated combination of a field name and an ordering directive ("ASC" or "DESC").
                     The default ordering is ["last_updated_timestamp DESC", "name ASC", "version_number DESC"].
    :raises MlflowException: If the entity in the ordering instruction is not 'attribute'.
    :return: A list of strings that can be used as arguments for MongoDB's order_by function.
             Each string starts with '+' for ascending order and '-' for descending order.
    """

    order_by_clauses = []
    for type_, key, ascending in map(
        SearchModelVersionUtils.parse_order_by_for_search_model_versions,
        order_by or ["last_updated_timestamp DESC", "name ASC", "version_number DESC"],
    ):
        if type_ == "attribute":
            order_by_clauses.append((key, ascending))
        else:
            raise MlflowException.invalid_parameter_value(
                f"Invalid order_by entity: {type_}"
            )

    # Add a tie-breaker
    if not any(col == "name" for col, _ in order_by_clauses):
        order_by_clauses.append(("name", False))

    return [_order_by_clause(col, ascending) for col, ascending in order_by_clauses]


def _get_search_registered_model_order_by_clauses(order_by):
    """
    Constructs a list of sorting directives based on the provided ordering instructions.

    :param order_by: A list of strings specifying the ordering of the returned registered models.
                     Each string is a space-separated combination of a field name and an ordering directive ("ASC" or "DESC").
                     The default ordering is ["last_updated_timestamp DESC", "name ASC"].
    :raises MlflowException: If the entity in the ordering instruction is not 'attribute'.
    :return: A list of strings that can be used as arguments for MongoDB's order_by function.
             Each string starts with '+' for ascending order and '-' for descending order.
    """

    order_by_clauses = []
    for type_, key, ascending in map(
        SearchModelUtils.parse_order_by_for_search_registered_models,
        order_by or ["last_updated_timestamp DESC", "name ASC"],
    ):
        if type_ == "attribute":
            order_by_clauses.append((key, ascending))
        else:
            raise MlflowException.invalid_parameter_value(
                f"Invalid order_by entity: {type_}"
            )

    # Add a tie-breaker
    if not any(col == "name" for col, _ in order_by_clauses):
        order_by_clauses.append(("name", False))

    return [_order_by_clause(col, ascending) for col, ascending in order_by_clauses]


def _get_archive_existing_versions_parsed_filters(name, version, stage):
    """
    Constructs a filter that matches model versions with a given name and stage,
    but excludes a particular version.

    :param name: The name of the registered model.
    :param version: The version of the registered model to exclude from the filter.
    :param stage: The stage of the registered model versions to match.
                  This is converted to its canonical form before use.
    :return: A list of filter conditions. Each filter condition is a dictionary that specifies
             the type of attribute, the key (attribute name), comparator, and value to match against.
    """
    _filter = list()
    _filter.append(
        {
            "type": "attribute",
            "key": "registered_model_id",
            "comparator": "=",
            "value": name,
        }
    )
    _filter.append(
        {
            "type": "attribute",
            "key": "version",
            "comparator": "!=",
            "value": version,
        }
    )
    _filter.append(
        {
            "type": "attribute",
            "key": "current_stage",
            "comparator": "=",
            "value": get_canonical_stage(stage),
        }
    )
    return _filter


def _get_not_deleted_model_versions_parsed_filters(name, version):
    """
    Constructs a filter that matches a model version with a given name and version,
    and excludes those marked as deleted.

    :param name: The name of the registered model.
    :param version: The version of the registered model to match.
    :return: A list of filter conditions. Each filter condition is a dictionary that specifies
             the type of attribute, the key (attribute name), comparator, and value to match against.
             In this case, the filter conditions ensure that the 'registered_model_id' attribute equals
             the provided model name, the 'version' attribute equals the provided model version,
             and the 'current_stage' attribute does not equal 'STAGE_DELETED_INTERNAL'.
    """
    _filter = list()
    _filter.append(
        {
            "type": "attribute",
            "key": "registered_model_id",
            "comparator": "=",
            "value": name,
        }
    )
    _filter.append(
        {
            "type": "attribute",
            "key": "version",
            "comparator": "=",
            "value": version,
        }
    )
    _filter.append(
        {
            "type": "attribute",
            "key": "current_stage",
            "comparator": "!=",
            "value": STAGE_DELETED_INTERNAL,
        }
    )
    return _filter


class MongoStore(AbstractStore):
    def __init__(self, store_uri: str) -> None:
        super(MongoStore, self).__init__()
        self.is_plugin = True

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

    @classmethod
    def create_registered_model(cls, name, tags=None, description=None):
        """
        Create a new registered model in backend store.

        :param name: Name of the new model. This is expected to be unique in the backend store.
        :param tags: A list of :py:class:`mlflow.entities.model_registry.RegisteredModelTag`
                     instances associated with this registered model.
        :param description: Description of the version.
        :return: A single object of :py:class:`mlflow.entities.model_registry.RegisteredModel`
                 created in the backend.
        """

        try:
            _validate_model_name(name)
            for tag in tags or []:
                _validate_registered_model_tag(tag.key, tag.value)

            creation_time = get_current_time_millis()

            mongo_registered_model = MongoRegisteredModel(
                name=name,
                creation_timestamp=creation_time,
                last_updated_timestamp=creation_time,
                description=description,
                tags=tags,
            )

            mongo_registered_model.save()
            return mongo_registered_model.to_mlflow_entity()
        except NotUniqueError as e:
            raise MlflowException(
                "Registered Model (name={}) already exists. Error: {}".format(
                    name, str(e)
                ),
                RESOURCE_ALREADY_EXISTS,
            )

    def update_registered_model(self, name, description):
        """
        Update description of the registered model.

        :param name: Registered model name.
        :param description: New description.
        :return: A single updated :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """

        mongo_registered_model = self._get_registered_model(name)
        updated_time = get_current_time_millis()
        mongo_registered_model.update(
            description=description, last_updated_timestamp=updated_time
        )
        mongo_registered_model.reload()
        return mongo_registered_model.to_mlflow_entity()

    def rename_registered_model(self, name, new_name):
        """
        Rename the registered model.

        :param name: Registered model name.
        :param new_name: New proposed name.
        :return: A single updated :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """

        try:
            mongo_registered_model = self._get_registered_model(name)
            mongo_models_versions, _ = self._search_model_versions(
                filter_string="name='" + name + "'",
            )
            with self.__db.client.start_session() as session:
                with session.start_transaction():

                    updated_time = get_current_time_millis()
                    mongo_registered_model.update(
                        name=new_name, last_updated_timestamp=updated_time
                    )
                    for mongo_models_version in mongo_models_versions:
                        mongo_models_version.update(
                            registered_model_id=new_name,
                            last_updated_timestamp=updated_time,
                        )

        except Exception as e:
            raise MlflowException(f"An error occurred during the rename: {str(e)}")

        mongo_registered_model.reload()
        return mongo_registered_model.to_mlflow_entity()

    def delete_registered_model(self, name):
        """
        Delete the registered model.
        Backend raises exception if a registered model with given name does not exist.

        :param name: Registered model name.
        :return: None
        """
        mongo_registered_model = self._get_registered_model(name)
        mongo_registered_model.delete()

    @classmethod
    def _get_registered_model(cls, name: str) -> MongoRegisteredModel:
        """
        Get registered model instance by name.

        :param name: Registered model name.
        :return: A single :py:class:`MongoRegisteredModel` object.
        """
        _validate_model_name(name)
        mongo_registered_models = MongoRegisteredModel.objects(name=name)

        if len(mongo_registered_models) == 0:
            raise MlflowException(
                "RegisteredModel with name={} not found".format(name),
                RESOURCE_DOES_NOT_EXIST,
            )
        if len(mongo_registered_models) > 1:
            raise MlflowException(
                "Expected only 1 RegisteredModel with name={}. Found {}.".format(
                    name, len(mongo_registered_models)
                ),
                INVALID_STATE,
            )

        return mongo_registered_models[0]

    def search_registered_models(
        self,
        filter_string=None,
        max_results=SEARCH_REGISTERED_MODEL_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search for registered models in backend that satisfy the filter criteria.

        :param filter_string: Filter query string, defaults to searching all registered models.
        :param max_results: Maximum number of registered models desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_registered_models`` call.
        :return: A PagedList of :py:class:`mlflow.entities.model_registry.RegisteredModel` objects
                that satisfy the search expressions. The pagination token for the next page can be
                obtained via the ``token`` attribute of the object.
        """

        def compute_next_token(current_size):
            next_token = None
            if max_results + 1 == current_size:
                final_offset = offset + max_results
                next_token = SearchUtils.create_page_token(final_offset)
            return next_token

        if not isinstance(max_results, int) or max_results < 1:
            raise MlflowException(
                "Invalid value for max_results. It must be a positive integer,"
                f" but got {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        if max_results > SEARCH_REGISTERED_MODEL_MAX_RESULTS_THRESHOLD:
            raise MlflowException(
                "Invalid value for request parameter max_results. It must be at most "
                f"{SEARCH_REGISTERED_MODEL_MAX_RESULTS_THRESHOLD}, but got value {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        parsed_filters = SearchModelUtils.parse_search_filter(filter_string)
        _filter = _get_search_registered_model_filter_clauses(parsed_filters)

        order_by_clauses = _get_search_registered_model_order_by_clauses(order_by)
        offset = SearchUtils.parse_start_offset_from_page_token(page_token)

        mongo_registered_models = MongoRegisteredModel.objects(_filter).order_by(
            *order_by_clauses
        )[offset : max_results + offset + 1]
        registered_models = [e.to_mlflow_entity() for e in mongo_registered_models]
        next_page_token = compute_next_token(len(registered_models))

        for registered_model in registered_models:
            registered_model.latest_versions = self.search_model_versions(
                filter_string="name='" + registered_model.name + "'",
                max_results=1,
                order_by=["version_number DESC"],
            )
            if len(registered_model.latest_versions) > 0:
                registered_model.last_updated_timestamp = (
                    registered_model.latest_versions[0].last_updated_timestamp
                )

        return PagedList(registered_models[:max_results], next_page_token)

    def get_registered_model(self, name):
        """
        Get registered model instance by name.

        :param name: Registered model name.
        :return: A single :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """
        return self._get_registered_model(name).to_mlflow_entity()

    def _get_latest_versions(self, name, stages=None):
        """
        Latest version models for each requested stage. If no ``stages`` argument is provided,
        returns the latest version for each stage.

        :param name: Registered model name.
        :param stages: List of desired stages. If input list is None, return latest versions for
                       each stage.
        :return: List of :py:class:`MongoModelVersion` objects.
        """

        # registered_model = self._get_registered_model(name)
        mongo_model_versions, _ = self._search_model_versions(
            filter_string="name='" + name + "'"
        )

        latest_versions = {}
        for mv in mongo_model_versions:
            stage = mv.current_stage
            if stage != STAGE_DELETED_INTERNAL and (
                stage not in latest_versions
                or latest_versions[stage].version < mv.version
            ):
                latest_versions[stage] = mv

        if stages is None or len(stages) == 0:
            expected_stages = {get_canonical_stage(stage) for stage in ALL_STAGES}
        else:
            expected_stages = {get_canonical_stage(stage) for stage in stages}

        return [mv for mv in latest_versions if mv.current_stage in expected_stages]

    def get_latest_versions(self, name, stages=None):
        """
        Latest version models for each requested stage. If no ``stages`` argument is provided,
        returns the latest version for each stage.

        :param name: Registered model name.
        :param stages: List of desired stages. If input list is None, return latest versions for
                       each stage.
        :return: List of :py:class:`mlflow.entities.model_registry.ModelVersion` objects.
        """
        mongo_latest_versions = self._get_latest_versions(name, stages)
        return [mv.to_mlflow_entity() for mv in mongo_latest_versions]

    def set_registered_model_tag(self, name, tag):
        """
        Set a tag for the registered model.

        :param name: Registered model name.
        :param tag: :py:class:`mlflow.entities.model_registry.RegisteredModelTag` instance to log.
        :return: None
        """

        _validate_model_name(name)
        _validate_registered_model_tag(tag.key, tag.value)
        mongo_registered_model = self._get_registered_model(name)
        mongo_registered_model.update(
            push__tags=MongoRegisteredModelTag(key=tag.key, value=tag.value)
        )

    def delete_registered_model_tag(self, name, key):
        """
        Delete a tag associated with the registered model.

        :param name: Registered model name.
        :param key: Registered model tag key.
        :return: None
        """
        _validate_model_name(name)
        _validate_tag_name(key)
        mongo_registered_model = self._get_registered_model(name)
        tags = mongo_registered_model.get_tags_by_key(key)
        if len(tags) == 0:
            raise MlflowException(
                f"No tag with name: {name} in RegisteredModel with key {key}",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )
        elif len(tags) > 1:
            raise MlflowException(
                "Bad data in database - tags for a specific RegisteredModel must have "
                "a single unique value. "
                "See https://mlflow.org/docs/latest/tracking.html#adding-tags-to-runs",
                error_code=INVALID_STATE,
            )
        mongo_registered_model.update(pull__tags=tags[0])

    def create_model_version(
        self, name, source, run_id=None, tags=None, run_link=None, description=None
    ):
        def next_version():
            if mongo_model_versions:
                return max([mv.version for mv in mongo_model_versions]) + 1
            else:
                return 1

        _validate_model_name(name)

        creation_time = get_current_time_millis()

        tags_dict = {}
        if tags is not None:
            for tag in tags:
                _validate_model_version_tag(tag.key, tag.value)
                tags_dict[tag.key] = tag.value
        exp_tags = [
            MongoModelVersionTag(key=key, value=value)
            for key, value in tags_dict.items()
        ]

        try:

            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    mongo_registered_model = self._get_registered_model(name)
                    mongo_model_versions, _ = self._search_model_versions(
                        filter_string="name='" + name + "'"
                    )
                    version = next_version()
                    mongo_registered_model.update(last_updated_timestamp=creation_time)
                    mongo_model_version = MongoModelVersion(
                        registered_model_id=name,
                        version=version,
                        creation_timestamp=creation_time,
                        last_updated_timestamp=creation_time,
                        source=source,
                        run_id=run_id,
                        run_link=run_link,
                        description=description,
                        tags=exp_tags,
                    )
                    mongo_model_version.save()

            return mongo_model_version.to_mlflow_entity()

        except Exception as e:
            raise MlflowException(
                f"Model Version creation error (name={name}): {str(e)}"
            )

    def update_model_version(self, name, version, description=None):
        """
        Update metadata associated with a model version in backend.

        :param name: Registered model name.
        :param version: Registered model version.
        :param description: New model description.
        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        mongo_model_version = self._get_model_version(name, version)
        updated_time = get_current_time_millis()
        mongo_model_version.update(
            description=description, last_updated_timestamp=updated_time
        )
        mongo_model_version.reload()
        return mongo_model_version.to_mlflow_entity()

    def delete_model_version(self, name, version):
        """
        Delete model version in backend.

        :param name: Registered model name.
        :param version: Registered model version.
        :return: None
        """
        mongo_registered_model = self._get_model_version(name, version)
        updated_time = get_current_time_millis()
        mongo_registered_model.update(
            last_updated_timestamp=updated_time,
            current_stage=STAGE_DELETED_INTERNAL,
            description=None,
            user_id=None,
            source="REDACTED-SOURCE-PATH",
            run_id="REDACTED-RUN-ID",
            run_link="REDACTED-RUN-LINK",
            status_message=None,
        )

    def get_model_version(self, name, version):
        """
        Get the model version instance by name and version.

        :param name: Registered model name.
        :param version: Registered model version.
        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        mongo_model_version = self._get_model_version(name, version)
        return mongo_model_version.to_mlflow_entity()

    def get_model_version_download_uri(self, name, version):
        """
        Get the download location in Model Registry for this model version.
        NOTE: For first version of Model Registry, since the models are not copied over to another
              location, download URI points to input source path.

        :param name: Registered model name.
        :param version: Registered model version.
        :return: A single URI location that allows reads for downloading.
        """
        mongo_model_version = self._get_model_version(name, version)
        return mongo_model_version.source

    @classmethod
    def search_model_versions(
        cls,
        filter_string=None,
        max_results=SEARCH_MODEL_VERSION_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search for model versions in backend that satisfy the filter criteria.

        :param filter_string: A filter string expression. Currently supports a single filter
                              condition either name of model like ``name = 'model_name'`` or
                              ``run_id = '...'``.
        :param max_results: Maximum number of model versions desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_model_versions`` call.
        :return: A PagedList of :py:class:`mlflow.entities.model_registry.ModelVersion`
                 objects that satisfy the search expressions. The pagination token for the next
                 page can be obtained via the ``token`` attribute of the object.
        """

        mongo_model_versions, next_page_token = cls._search_model_versions(
            filter_string, max_results, order_by, page_token
        )
        model_versions = [e.to_mlflow_entity() for e in mongo_model_versions]

        return PagedList(model_versions[:max_results], next_page_token)

    @classmethod
    def _search_model_versions(
        cls,
        filter_string=None,
        max_results=SEARCH_MODEL_VERSION_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search for model versions in backend that satisfy the filter criteria.

        :param filter_string: A filter string expression. Currently supports a single filter
                              condition either name of model like ``name = 'model_name'`` or
                              ``run_id = '...'``.
        :param max_results: Maximum number of model versions desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_model_versions`` call.
        :return: A Tuple of :py:class:`MongoModelVersion`
                 objects that satisfy the search expressions. The pagination token for the next
                 page can be obtained via the ``token`` attribute of the object.
        """

        def compute_next_token(current_size):
            next_token = None
            if max_results + 1 == current_size:
                final_offset = offset + max_results
                next_token = SearchUtils.create_page_token(final_offset)

            return next_token

        if not isinstance(max_results, int) or max_results < 1:
            raise MlflowException(
                "Invalid value for max_results. It must be a positive integer,"
                f" but got {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        if max_results > SEARCH_MODEL_VERSION_MAX_RESULTS_THRESHOLD:
            raise MlflowException(
                "Invalid value for request parameter max_results. It must be at most "
                f"{SEARCH_MODEL_VERSION_MAX_RESULTS_THRESHOLD}, but got value {max_results}",
                INVALID_PARAMETER_VALUE,
            )

        parsed_filters = SearchModelVersionUtils.parse_search_filter(filter_string)
        _filter = _get_search_model_version_filter_clauses(parsed_filters)

        order_by_clauses = _get_search_model_version_order_by_clauses(order_by)
        offset = SearchUtils.parse_start_offset_from_page_token(page_token)

        mongo_model_versions = MongoModelVersion.objects(_filter).order_by(
            *order_by_clauses
        )[offset : max_results + offset + 1]
        next_page_token = compute_next_token(len(mongo_model_versions))

        return mongo_model_versions[:max_results], next_page_token

    def set_model_version_tag(self, name, version, tag):
        """
        Set a tag for the model version.

        :param name: Registered model name.
        :param version: Registered model version.
        :param tag: :py:class:`mlflow.entities.model_registry.ModelVersionTag` instance to log.
        :return: None
        """

        _validate_model_name(name)
        _validate_model_version(version)
        _validate_model_version_tag(tag.key, tag.value)

        mongo_model_version = self._get_model_version(name, version)
        mongo_model_version.update(
            push__tags=MongoModelVersionTag(key=tag.key, value=tag.value)
        )

    def delete_model_version_tag(self, name, version, key):
        """
        Delete a tag associated with the model version.

        :param name: Registered model name.
        :param version: Registered model version.
        :param key: Tag key.
        :return: None
        """
        _validate_model_name(name)
        _validate_model_version(version)
        _validate_tag_name(key)
        mongo_model_version = self._get_model_version(name, version)
        tags = mongo_model_version.get_tags_by_key(key)
        if len(tags) == 0:
            raise MlflowException(
                f"No tag with name: {name} in ModelVersion with key {key}",
                error_code=RESOURCE_DOES_NOT_EXIST,
            )
        elif len(tags) > 1:
            raise MlflowException(
                "Bad data in database - tags for a specific RegisteredModel must have "
                "a single unique value. "
                "See https://mlflow.org/docs/latest/tracking.html#adding-tags-to-runs",
                error_code=INVALID_STATE,
            )
        mongo_model_version.update(pull__tags=tags[0])

    @classmethod
    def _get_model_version(cls, name, version) -> MongoModelVersion:
        """
        Get the model version instance by name and version.

        :param name: Registered model name.
        :param version: Registered model version.
        :return: A single :py:class:`MongoModelVersion` object.
        """

        _validate_model_name(name)
        _validate_model_version(version)

        _filter = _get_not_deleted_model_versions_parsed_filters(name, version)
        _filter = _get_search_model_version_filter_clauses(_filter)
        mongo_model_versions = MongoModelVersion.objects(_filter)

        if len(mongo_model_versions) == 0:
            raise MlflowException(
                "ModelVersion with name={} and version={) not found".format(
                    name, version
                ),
                RESOURCE_DOES_NOT_EXIST,
            )
        if len(mongo_model_versions) > 1:
            raise MlflowException(
                "Expected only 1 ModelVersion with name={} and version={). Found {}.".format(
                    name, version, len(mongo_model_versions)
                ),
                INVALID_STATE,
            )
        return mongo_model_versions[0]

    def transition_model_version_stage(
        self, name, version, stage, archive_existing_versions
    ):
        """
        Update model version stage.

        :param name: Registered model name.
        :param version: Registered model version.
        :param stage: New desired stage for this model version.
        :param archive_existing_versions: If this flag is set to ``True``, all existing model
            versions in the stage will be automatically moved to the "archived" stage. Only valid
            when ``stage`` is ``"staging"`` or ``"production"`` otherwise an error will be raised.

        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        is_active_stage = (
            get_canonical_stage(stage) in DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS
        )
        if archive_existing_versions and not is_active_stage:
            msg_tpl = (
                "Model version transition cannot archive existing model versions "
                "because '{}' is not an Active stage. Valid stages are {}"
            )
            raise MlflowException(
                msg_tpl.format(stage, DEFAULT_STAGES_FOR_GET_LATEST_VERSIONS)
            )

        try:
            with self.__db.client.start_session() as session:
                with session.start_transaction():
                    last_updated_time = get_current_time_millis()
                    if archive_existing_versions:
                        _filter = _get_archive_existing_versions_parsed_filters(
                            name, version, stage
                        )
                        _filter = _get_search_model_version_filter_clauses(_filter)
                        mongo_model_versions = MongoModelVersion.objects(_filter)
                        for mv in mongo_model_versions:
                            mv.update(
                                current_stage=STAGE_ARCHIVED,
                                last_updated_timestamp=last_updated_time,
                            )

                    mongo_model_version = self._get_model_version(
                        name=name, version=version
                    )
                    mongo_model_version.update(
                        last_updated_timestamp=last_updated_time,
                        current_stage=get_canonical_stage(stage),
                    )

                    mongo_registered_model = self._get_registered_model(name)
                    mongo_registered_model.update(
                        last_updated_timestamp=last_updated_time
                    )

                    return mongo_model_version.to_mlflow_entity()
        except Exception as e:
            raise MlflowException(f"An error occurred during the transition: {str(e)}")
