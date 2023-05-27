import atexit
import pkgutil
import kayaku
import creart
from kayaku import bootstrap, config, create, save_all
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
)
from graia.ariadne.connection.config import config as networkCFG
from graia.saya import Saya
from launart import Launart, LaunartBehaviour


kayaku.initialize(
    {
        "{**}": "./config/{**}",
        "{**}.credential": "./config/credential.jsonc::{**}"
    }
)
atexit.register(save_all)

saya = creart.it(Saya)
manager = Launart()
saya.install_behaviours(LaunartBehaviour(manager))

Ariadne.config(launch_manager=manager, install_log=True)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")


@config("platform.account.credential")
class Credential:
    account: int
    """The num of Accounts"""

    token: str
    """The verify token"""

    host: str
    """The mirai-api-http host"""


bootstrap()

cfg = create(Credential)
if not cfg.account:
    raise ValueError("No account configured.")

Ariadne(
    connection=networkCFG(
        cfg.account,
        cfg.token,
        HttpClientConfig(host=cfg.host),
        WebsocketClientConfig(host=cfg.host),
    )
)
Ariadne.launch_blocking()
