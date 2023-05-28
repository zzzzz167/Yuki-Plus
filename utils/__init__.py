from .database import DatabaseManager
from .config import basic_cfg

db = DatabaseManager(basic_cfg.databaseUrl)
