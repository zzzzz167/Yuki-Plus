import atexit
import pkgutil
import kayaku
import creart
from loguru import logger
from kayaku import bootstrap, save_all
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
)
from graia.ariadne.connection.config import config as networkCFG
from graia.saya import Saya
from arclet.alconna.graia.saya import AlconnaBehaviour
from launart import Launart, LaunartBehaviour


kayaku.initialize(
    {
        "{**}": "./config/{**}",
    }
)
atexit.register(save_all)
from utils.config import basic_cfg  # noqa: E402
from utils.launart_services import DatabaseInitService  # noqa: E402

saya = creart.it(Saya)
creart.it(AlconnaBehaviour)
manager = Launart()
saya.install_behaviours(LaunartBehaviour(manager))
manager.add_service(DatabaseInitService())
Ariadne.config(launch_manager=manager, install_log=True)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["cores"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")
logger.info("Core Loded!")


with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")
logger.info("Saya Modules Loded!")

bootstrap()

if basic_cfg.miraiApiHttp.account == 12345678:
    raise ValueError("Please rename bot account")

Ariadne(
    connection=networkCFG(
        basic_cfg.miraiApiHttp.account,
        basic_cfg.miraiApiHttp.verifyKey,
        HttpClientConfig(host=basic_cfg.miraiApiHttp.host),
        WebsocketClientConfig(host=basic_cfg.miraiApiHttp.host),
    )
)
logger.add(
    "./cache/logs/debuglogs", rotation="00:00", retention="10 days", compression="zip"
)


Ariadne.launch_blocking()
