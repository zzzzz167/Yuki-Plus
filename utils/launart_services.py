from typing import Literal, Union
from launart import ExportInterface, Launchable
from loguru import logger
from . import db


class DatabaseInitService(Launchable):
    id: str = 'database/init'

    @property
    def required(self) -> set[Union[str, type[ExportInterface]]]:
        return set()

    @property
    def stages(self) -> set[Literal['preparing', 'blocking', 'cleanup']]:
        return set()

    async def launch(self, _):
        logger.info('Initializing database...')
        await db.initialize()
