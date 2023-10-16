from abc import ABC
from typing import TypeVar, Callable, Awaitable
from dataclasses import is_dataclass, field, fields, Field

from graphql import GraphQLResolveInfo
import pypika
from pypika.queries import QueryBuilder


class ValueEnum:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return self.__dict__[item]

    def __getitem__(self, item):
        return self.__dict__[item]


class Registry:
    def __init__(
            self,
            query_class: type[pypika.Query] = pypika.Query,
            schema_name: str | None = None,
            custom_loader: Callable[[GraphQLResolveInfo, QueryBuilder], Awaitable[list]] | None = None
    ):
        self.schema_name = schema_name
        self.models = []
        self.custom_loader = custom_loader
        self.query_class = query_class


class ModelMetaData:
    def __init__(
            self,
            registry: Registry,
            table_name: str,
            primary_keys: list[str],
            table: pypika.Table,
            dataclass_fields: dict[str, Field],
            database_fields: dict[str, pypika.Field],
            relations: dict[str, 'Relation']
    ):
        self.registry = registry
        self.table_name = table_name
        self.primary_keys = primary_keys
        self.table = table
        self.dataclass_fields = dataclass_fields
        self.database_fields = database_fields
        self.database_fields_list = list(database_fields.values())
        self.relations = relations

        self.field_count = len(self.database_fields)


class BaseModel(ABC):
    __metadata__: ModelMetaData


T = TypeVar('T')


def database_model(
        registry: Registry,
        table_name: str,
        primary_keys: list[str],
):
    def database_model_sub(cls: type[T]) -> type[T]:
        assert is_dataclass(cls)

        # Collect Fields
        dc_fields = fields(cls)

        # Check primary keys
        for pk in primary_keys:
            if pk not in [f.name for f in dc_fields]:
                raise TypeError(f"primary key column '{pk}' not found in {cls.__name__}")

        database_table = pypika.Table(table_name, registry.schema_name)

        # Build fields
        dataclass_fields = {}
        database_fields = {}
        for dc_field in dc_fields:
            field_name = dc_field.name
            db_real_name = dc_field.metadata.get('db_name', field_name)
            # Todo: Make sure works when aliasing
            table_field = pypika.Field(db_real_name, field_name if field_name != db_real_name else None, database_table)
            setattr(cls, field_name, table_field)  # After dataclass processing, reset class attibutes
            dataclass_fields[field_name] = dc_field
            database_fields[field_name] = table_field

        # Check relations
        # if not hasattr(cls, 'relations'):
        #     cls.relations = {}
        # for relation in cls.relations.values():
        #     cls._check_relation(relation)

        assert issubclass(cls, BaseModel)

        metadata = ModelMetaData(
            registry, table_name, primary_keys,
            database_table, dataclass_fields, database_fields,
            {}  # Todo, handle relations
        )

        cls.__metadata__ = metadata

        # Add to registry
        registry.models.append(cls)

        return cls
    return database_model_sub


class Relation:
    def __init__(self, model, **join_on: str):
        if not len(join_on):
            raise Exception("There has to be at least one join condition")

        join_fields = model.__metadata__.database_fields.keys()
        for join_field in join_on:
            if join_field not in join_fields:
                raise Exception(f"Field {join_field} does not exist in {model.__name__}")

        self.model = model
        self.join_on = join_on


def _check_relation(cls, relation: Relation):
    local_fields = cls.database_fields.keys()
    for local_field in relation.join_on.values():
        if local_field not in local_fields:
            raise Exception(f"Field {local_field} does not exist in {cls.__name__}")


def db_name(val: str):
    return field(metadata={'db_name': val})
