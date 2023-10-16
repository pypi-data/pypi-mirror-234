from typing import AsyncContextManager
import asyncio
import json
import contextlib

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import asyncpg
from asyncpg.exceptions import PostgresError
from pypika.queries import QueryBuilder


async def setup_jsonb_codec(conn: asyncpg.Connection):
    await conn.set_type_codec(
        "jsonb",
        encoder=json.dumps,
        decoder=json.loads,
        schema="pg_catalog",
    )


class LockedDB:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn
        self.lock = asyncio.Lock()

    async def execute(self, query: str | QueryBuilder, *args, timeout: float | None = None) -> str:
        async with self.lock:
            return await self.conn.execute(str(query), *args, timeout=timeout)

    async def executemany(self, command: str | QueryBuilder, args, *, timeout: float | None = None):
        async with self.lock:
            return await self.conn.executemany(str(command), args, timeout=timeout)

    async def fetch(self, query: str | QueryBuilder, *args, timeout=None, record_class=None) -> list[asyncpg.Record]:
        async with self.lock:
            return await self.conn.fetch(str(query), *args, timeout=timeout, record_class=record_class)

    async def fetchrow(self, query: str | QueryBuilder, *args, timeout=None, record_class=None) -> asyncpg.Record | None:
        async with self.lock:
            return await self.conn.fetchrow(str(query), *args, timeout=timeout, record_class=record_class)

    async def fetchval(self, query: str | QueryBuilder, *args, column=0, timeout=None):
        async with self.lock:
            return await self.conn.fetchval(str(query), *args, column=column, timeout=timeout)


async def create_pool(database_uri):
    return await asyncpg.create_pool(database_uri, init=setup_jsonb_codec,
                                     timeout=5, max_size=5, max_inactive_connection_lifetime=100)


@contextlib.asynccontextmanager
async def get_transactional_db(request: Request) -> AsyncContextManager[LockedDB]:
    async with request.app.state.db_pool.acquire() as connection:
        transaction = connection.transaction()
        await transaction.start()

        yield LockedDB(connection)

        try:  # Try to commit
            await transaction.commit()
        except PostgresError:
            await transaction.rollback()
            raise


class AsyncDBMiddleware(BaseHTTPMiddleware):
    """ Will start a DB Session at every request and commit or rollback in the end """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        async with request.app.state.db_pool.acquire() as connection:
            transaction = connection.transaction()
            await transaction.start()
            request.state.db = LockedDB(connection)

            # Continue with request
            response = await call_next(request)

            if hasattr(request.state, 'errors'):
                await transaction.rollback()
            else:
                try:  # Try to commit
                    await transaction.commit()
                except PostgresError:
                    await transaction.rollback()
                    return JSONResponse({'errors': [{'message': "Error while commiting to Database"}]}, status_code=500)
            return response
