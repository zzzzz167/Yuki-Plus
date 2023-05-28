from importlib import metadata
from .database import DatabaseManager
from .config import basic_cfg

db = DatabaseManager(basic_cfg.databaseUrl)


def get_graia_version():
    extra: list[tuple[str, str]] = []
    official: list[tuple[str, str]] = []
    community: list[tuple[str, str]] = []

    for dist in metadata.distributions():
        name: str = dist.metadata['Name']
        version: str = dist.version
        if name in {'launart', 'creart', 'creart-graia', 'statv', 'richuru'}:
            extra.append((name, version))
        elif name.startswith('graia-'):
            official.append((name, version))
        elif name.startswith('graiax-'):
            community.append((name, version))

    return extra, official, community
