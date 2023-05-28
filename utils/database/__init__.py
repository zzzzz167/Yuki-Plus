import contextlib
from asyncio import current_task
from typing import Union, Any, Sequence
from sqlalchemy.engine import Row
from sqlalchemy.engine.url import URL
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.sql.base import Executable
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from .types import EngineOptions
from .models import Base


class DatabaseManager:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(
        self, url: Union[str, URL], engin_options: Union[EngineOptions, None] = None
    ):
        if engin_options is None:
            engine_options = {
                "echo": True,
                "pool_pre_ping": True,
            }
        self.engine = create_async_engine(url, **engine_options)

    async def initialize(self, session_options: Union[dict[str, Any], None] = None):
        if session_options is None:
            session_options = {"expire_on_commit": False}
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.session_factory = async_sessionmaker(self.engine, **session_options)

    async def stop(self):
        # for AsyncEngine created in function scope, close and
        # clean-up pooled connections
        await self.engine.dispose()

    async def async_safe_session(self):
        """
        生成一个异步安全的session回话
        :return:
        """
        self._scoped_session = async_scoped_session(
            self.session_factory, scopefunc=current_task
        )
        return self._scoped_session

    @contextlib.asynccontextmanager
    async def async_session(self):
        """
        异步session上下文管理封装
        :return:
        >>> async with db_manager.async_session() as session:
        >>>     res = await session.execute("SELECT 1")
        >>>     print(res.scalar())
        1
        """
        scoped_session = await self.async_safe_session()
        try:
            yield scoped_session
            await self._scoped_session.commit()
        except Exception:
            await self._scoped_session.rollback()
            raise
        finally:
            await self._scoped_session.remove()

    async def exec(self, sql: Executable) -> Result:
        async with self.async_session() as session:
            return await session.execute(sql)

    async def select_all(self, sql: Executable) -> Sequence[Row]:
        result = await self.exec(sql)
        return result.all()

    async def select_first(self, sql: Executable) -> Union[Row, None]:
        result = await self.exec(sql)
        return result.first()

    async def add(self, row):
        scoped_session = await self.async_safe_session()
        try:
            scoped_session.add(row)
            await self._scoped_session.commit()
            await self._scoped_session.refresh(row)
        except Exception:
            await self._scoped_session.rollback()
            raise
        finally:
            await self._scoped_session.remove()

    async def add_many(self, rows: Sequence[Base]):
        scoped_session = await self.async_safe_session()
        try:
            scoped_session.add_all(rows)
            await self._scoped_session.commit()
            for row in rows:
                await self._scoped_session.refresh(row)
        except Exception:
            await self._scoped_session.rollback()
            raise
        finally:
            await self._scoped_session.remove()

    async def update_or_add(self, row):
        scoped_session = await self.async_safe_session()
        try:
            await scoped_session.merge(row)
            await self._scoped_session.commit()
            # await self._scoped_session.refresh(row)
        except Exception:
            await self._scoped_session.rollback()
            raise
        finally:
            await self._scoped_session.remove()

    async def delete_exist(self, row):
        async with self.async_session() as session:
            await session.delete(row)

    async def delete_many_exist(self, *rows):
        async with self.async_session() as session:
            for row in rows:
                await session.delete(row)
