from dataclasses import astuple
from decimal import Decimal
from types import UnionType
from typing import get_type_hints, get_origin, get_args, Sequence, Iterable, Mapping

from graphql import GraphQLResolveInfo
import pypika
from aiodataloader import DataLoader
from asyncpg import Connection
from pypika.queries import QueryBuilder

from ..database import LockedDB
from ..exceptions import NoRowsError, MultipleRowsError, DatabaseQueryError
from ..models_utils import T
from ..request_utils import get_state, get_db


def table(model: type[T]) -> pypika.Table:
    return model.__metadata__.table


def all_fields(model: type[T]) -> list[pypika.Field]:
    return model.__metadata__.database_fields_list


def build_from_tuple(model: type[T], rec: Sequence | None) -> T | None:
    if rec is None:
        return None
    return model(*rec)


def build_from_mapping(model: type[T], rec: Mapping | None) -> T | None:
    if rec is None:
        return None
    return model(**rec)


def build(model: type[T], rec) -> T | None:
    try:
        return build_from_mapping(model, rec)
    except TypeError:
        return build_from_tuple(model, rec)


def build_all(model: type[T], recs: Sequence) -> list[T]:
    try:
        return [build_from_mapping(model, rec) for rec in recs]
    except TypeError:
        return [build_from_tuple(model, rec) for rec in recs]


def primary_key_filter(model: type[T], primary_keys: Sequence) -> pypika.Criterion:
    """ Return Criterion to be used in a .where() """
    if not len(primary_keys):
        raise DatabaseQueryError("Primary key filter must have at least one value")
    conditions = [
        getattr(model, model.__metadata__.primary_keys[i]) == pk_value
        for i, pk_value in enumerate(primary_keys)
    ]
    return pypika.Criterion.all(conditions)


def get_query(model: type[T], primary_keys: Sequence) -> QueryBuilder:
    """ Primary keys can be Params """
    q = model.__metadata__.registry.query_class.from_(table(model)).select(*all_fields(model)).where(primary_key_filter(model, primary_keys))
    return q


async def get(db: Connection | LockedDB, model: type[T], primary_keys: Sequence) -> T | None:
    """ Primary keys need to be real values """
    pk_params = [pypika.Parameter(f'${i+1}') for i in range(len(primary_keys))]
    q = get_query(model, pk_params)
    rows = await db.fetch(q, *primary_keys)
    row_count = len(rows)
    if row_count == 0:
        return None
    if row_count > 1:
        raise MultipleRowsError
    return build_from_mapping(model, rows[0])


async def get_or_error(db: Connection | LockedDB, model: type[T], primary_keys: Sequence) -> T:
    """ Primary keys need to be real values """
    row = await get(db, model, primary_keys)
    if row is None:
        raise NoRowsError
    return row


def delete_query(model: type[T], primary_keys: Sequence) -> QueryBuilder:
    """ Primary keys can be Params """
    metadata = model.__metadata__
    if len(primary_keys) != len(metadata.primary_keys):
        raise DatabaseQueryError("Primary keys argument in BaseModel.delete_query() must match BaseModel's in length")
    q = metadata.registry.query_class.from_(table(model)).delete().where(primary_key_filter(model, primary_keys))
    return q


async def delete(db: Connection | LockedDB, model: type[T], primary_keys: Sequence) -> None:
    """ Primary keys need to be real values """
    pk_params = [pypika.Parameter(f'${i + 1}') for i in range(len(primary_keys))]
    q = delete_query(model, pk_params)
    await db.execute(q, *primary_keys)


def insert_query(
        model: type[T],
        start_number: int | None = 1,
        placeholder: str = '${}'
) -> QueryBuilder:
    """ Assuming order of values is the same as order of astuples(dataclass) """
    return model.__metadata__.registry.query_class.into(table(model))\
        .columns(*all_fields(model))\
        .insert(*generate_params(model, start_number, placeholder))


async def insert(db: Connection | LockedDB, model: type[T], obj: T):
    await db.execute(insert_query(model), *astuple(obj))


async def insert_many(db: Connection | LockedDB, model: type[T], objs: Iterable[T]):
    await db.executemany(insert_query(model), [astuple(obj) for obj in objs])


def update_query(
        model: type[T],
        start_number: int | None = 1,
        placeholder: str = '${}'
) -> QueryBuilder:
    metadata = model.__metadata__
    params = generate_params(model, start_number, placeholder)
    q = metadata.registry.query_class.update(table(model))
    for field_name, db_field in model.__metadata__.database_fields.items():
        if field_name in metadata.primary_keys:
            q = q.where(db_field == params.pop(0))
        else:
            q = q.set(db_field, params.pop(0))
    return q


async def update(db: Connection | LockedDB, model: type[T], obj: T):
    await db.execute(update_query(model), *astuple(obj))


async def update_many(db: Connection | LockedDB, model: type[T], objs: Iterable[T]):
    await db.executemany(update_query(model), [astuple(obj) for obj in objs])


def join_relation(model: type[T], q: QueryBuilder, relation_name: str, join_type: pypika.JoinType = pypika.JoinType.inner) -> tuple[QueryBuilder, type[T]]:
    try:
        relation = model.__metadata__.relations[relation_name]
    except KeyError:
        raise Exception(f"Could not find Relation {relation_name} in model {model.__name__}")

    rel_model = relation.model

    if not q.is_joined(table(rel_model)):
        q = q.join(table(rel_model), join_type).on(pypika.Criterion.all([
            getattr(rel_model, rel_col) == getattr(model, local_col)
            for rel_col, local_col in relation.join_on.items()
        ]))

    return q, rel_model


def generate_params(model: type[T], start_number: int | None = 1, placeholder: str = '${}') -> list[pypika.Parameter]:
    return [
        pypika.Parameter(placeholder if start_number is None else placeholder.format(start_number + i))
        for i in range(model.__metadata__.field_count)
    ]


async def batch_get(info: GraphQLResolveInfo, model: type[T], keys_list: Sequence[tuple]) -> list[T | None]:
    metadata = model.__metadata__
    loader = metadata.registry.custom_loader or (lambda x, y: get_db(x).fetch(y))
    q = metadata.registry.query_class.from_(table(model)).select(*all_fields(model)).where(
        pypika.Tuple(*(getattr(model, pk) for pk in metadata.primary_keys)).isin(keys_list)
    )
    d = {tuple(getattr(obj, pk) for pk in metadata.primary_keys): obj for obj in build_all(model, await loader(info, q))}
    return [d.get(keys) for keys in keys_list]


async def dataloader_get(info: GraphQLResolveInfo, model: type[T], primary_keys: tuple) -> T | None:
    state = get_state(info)
    if not hasattr(state, 'auto_loaders'):
        state.auto_loaders = {}

    try:
        dl = state.auto_loaders[model.__name__]
    except KeyError:
        async def batch_get_wrapper(keys_list: Sequence[tuple]):
            return await batch_get(model, info, keys_list)  # attach info
        dl = state.auto_loaders[model.__name__] = DataLoader(batch_get_wrapper)
    return await dl.load(primary_keys)


def set_dataclass_attribute(obj, field_name: str, field_value):
    """ Like setattr but try to handle types"""
    field_type = get_type_hints(obj.__class__)[field_name]

    if get_origin(field_type) is UnionType:
        field_type = get_args(field_type)[0]

    if field_type is Decimal and isinstance(field_value, float):  # Convert float to Decimal
        field_value = Decimal(field_value)

    setattr(obj, field_name, field_value)


def get_field_main_type(model, field_name: str) -> type:
    type_ = model.__metadata__.dataclass_fields[field_name].type

    if get_origin(type_) is UnionType:
        type_ = get_args(type_)[0]

    if get_origin(type_) is list:
        return list

    return type_
