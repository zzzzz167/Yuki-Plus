from dataclasses import dataclass, field
from kayaku import config, create


@dataclass
class MAHConfig:
    account: int = 123456789
    """Mirai Api Http 已登录的账号"""
    host: str = "http://localhost:8080"
    """Mirai Api Http 地址"""
    verifyKey: str = "VerifyKey"
    """Mirai Api Http 的 verifyKey"""


@dataclass
class AdminConfig:
    masterId: int = 2742400566
    """机器人主人的QQ号"""
    admins: list[int] = field(default_factory=lambda: [2742400566])
    """机器人管理员列表"""


@config("bot")
class BasicConfig:
    debugLevel: str = "DEBUG"
    databaseUrl: str = "sqlite+aiosqlite:///data/database.db"
    """数据库地址"""
    miraiApiHttp: MAHConfig = MAHConfig()
    """Mirai Api Http 配置"""
    admin: AdminConfig = AdminConfig()
    """机器人管理相关配置"""


@config("modules")
class ModulesConfig:
    enabled: bool = True
    """是否允许加载模块"""

    globalDisabledModules: list[str] = field(default_factory=lambda: [])
    disabledGroups: dict[str, list[int]] = field(default_factory=lambda: {})


basic_cfg = create(BasicConfig)
modules_cfg = create(ModulesConfig, flush=True)
