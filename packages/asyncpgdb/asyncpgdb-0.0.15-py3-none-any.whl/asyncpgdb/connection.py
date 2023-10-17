from typing import Any, Optional, Type, Union
from logging import Logger
from asyncpgdb.asyncpg import ConnectionAsyncpg, connect
from asyncpgdb.execute import ExecuteProtocol
from asyncpgdb.dsn import create_dsn
from asyncpgdb.settings import Settings


class Connection(ExecuteProtocol):
    def __init__(
        self,
        dsn: Optional[str] = None,
        *,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        passfile: Optional[str] = None,
        database: Optional[str] = None,
        loop: Optional[Any] = None,
        timeout: Optional[float] = 60,
        statement_cache_size: Optional[int] = 100,
        max_cached_statement_lifetime: Optional[float] = 300,
        max_cacheable_statement_size: Optional[int] = 1024 * 15,
        command_timeout: Optional[float] = None,
        ssl: Optional[str] = None,
        direct_tls: bool = False,
        connection_class: Type[ConnectionAsyncpg] = ConnectionAsyncpg,
        record_class: Optional[Type] = None,
        server_settings: Optional[dict] = None,
        conn: Optional[ConnectionAsyncpg] = None,
        logger: Optional[Logger] = None,
    ):
        if not dsn:
            dsn = create_dsn(
                host=host, port=port, user=user, password=password, database=database
            )
        self._settings = Settings(
            dsn=dsn,
            host=host,
            port=port,
            user=user,
            password=password,
            passfile=passfile,
            database=database,
            loop=loop,
            timeout=timeout,
            statement_cache_size=statement_cache_size,
            max_cacheable_statement_size=max_cacheable_statement_size,
            max_cached_statement_lifetime=max_cached_statement_lifetime,
            command_timeout=command_timeout,
            ssl=ssl,
            direct_tls=direct_tls,
            connection_class=connection_class,
            record_class=record_class,
            server_settings=server_settings,
        )
        self._connect_kwargs = self._settings.connection_connect_kwargs()

        self._conn = conn
        self._logger = logger

    async def acquire_connection(self) -> ConnectionAsyncpg:
        if self._conn is None or self._conn.is_closed():
            self._conn = await connect(**self._connect_kwargs())

        return self._conn

    async def close(self):
        if self._conn is not None and not self._conn.is_closed():
            await self._conn.close()
            self._conn = None

    async def release(self, __conn: ConnectionAsyncpg):
        pass
