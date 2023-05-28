import os
import time
import psutil
import platform
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from arclet.alconna import Alconna
from arclet.alconna.graia.dispatcher import AlconnaDispatcher
from graia.saya import Channel
from graiax.shortcut.saya import listen, dispatch
from utils import get_graia_version
from utils.text2img import md2img

channel = Channel.current()
channel.name("运行状态")
channel.description("Bot版本与系统运行情况查询")
statusALC = Alconna(".status")

extra, official, community = get_graia_version()
python_version = platform.python_version()
if platform.uname().system == "Windows":
    system_version = platform.platform()
else:
    system_version = f"{platform.platform()} {platform.version()}"
total_memory = "%.1f" % (psutil.virtual_memory().total / 1073741824)
pid = os.getpid()


@listen(GroupMessage)
@dispatch(AlconnaDispatcher(statusALC, send_flag="reply"))
async def cheak_status(app: Ariadne, group: Group):
    p = psutil.Process(pid)
    started_time = time.localtime(p.create_time())
    running_time = time.time() - p.create_time()
    day = int(running_time / 86400)
    hour = int(running_time % 86400 / 3600)
    minute = int(running_time % 86400 % 3600 / 60)
    second = int(running_time % 86400 % 3600 % 60)
    running_time = f'{f"{day}d " if day else ""}{f"{hour}h " if hour else ""}{f"{minute}m " if minute else ""}{second}s'
    md = f'''\
<div align="center">

# Yuki 状态

</div>

## 基本信息
**PID**: {pid}
**启动时间**: {time.strftime("%Y-%m-%d %p %I:%M:%S", started_time)}
**已运行时长**: {running_time}

## 运行环境
**Python 版本**: {python_version}
**系统版本**: {system_version}
**CPU 核心数**: {psutil.cpu_count()}
**CPU 占用率**: {psutil.cpu_percent()}%
**系统内存占用**: {"%.1f" % (psutil.virtual_memory().available / 1073741824)}G / {total_memory}G

## 依赖版本
**Mirai Api Http**: {await app.get_version()}
**Graia 相关**:
'''
    if extra:
        md += ''.join(f'  - {name}: {version}\n' for name, version in extra)
    md += ''.join(f'  - {name}: {version}\n' for name, version in official)
    if community:
        md += ''.join(f'  - {name}: {version}\n' for name, version in community)

    await app.send_message(group, MessageChain(Image(data_bytes=await md2img(md.rstrip()))))
