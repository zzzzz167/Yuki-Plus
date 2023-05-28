import random
from loguru import logger
from typing import Sequence
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image
from graia.saya import Channel
from arclet.alconna import Alconna, CommandMeta
from arclet.alconna.graia.dispatcher import AlconnaDispatcher
from graiax.shortcut.saya import listen, dispatch
from sqlalchemy.sql import select
from utils import db
from utils.database.models import User
from .image import getMaskBg

channel = Channel.current()
channel.name("签到")
channel.description("每日签到")

signALC = Alconna(".sign", meta=CommandMeta("每日签到"))


@listen(GroupMessage)
@dispatch(AlconnaDispatcher(signALC, send_flag="reply"))
async def sign_in(app: Ariadne, group: Group, member: Member):
    result: Sequence[User] = await db.select_first(
        select(User).where(User.qq == member.id)
    )

    if result is None:
        await db.add(User(qq=member.id))
        logger.info(f"为 {member.name}({member.id}) 新建了配置")
        result = await db.select_first(select(User).where(User.qq == member.id))

    if result[0].today:
        await app.send_group_message(
            group, MessageChain([Plain("今天你已经签到过啦,不要做贪心鬼哦,明天再来吧")])
        )
        return

    favor = result[0].favor + random.randint(0, 5)
    days = result[0].days + 1

    await app.send_group_message(
        group,
        MessageChain(
            [Image(data_bytes=await getMaskBg(member.id, member.name, days, favor, "Hello world"))]
        ),
    )

    await db.update_or_add(User(qq=result[0].qq, favor=favor, days=days, today=True))
