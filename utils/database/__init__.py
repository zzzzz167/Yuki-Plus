from typing import Union, Any
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from .types import EngineOptions
from .models import Base


class DatabaseManager:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, url: Union[str, URL], engin_options: Union[EngineOptions, None] = None):
        if engin_options is None:
            engine_options = {"echo": "debug", "pool_pre_ping": True}
        self.engine = create_async_engine(url, **engine_options)

    async def initialize(self, session_options: Union[dict[str, Any], None] = None):
        if session_options is None:
            session_options = {'expire_on_commit': False}
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.session_factory = async_sessionmaker(self.engine, **session_options)
