import json
import random
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import At
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from arclet.alconna import Alconna, Args, Empty, CommandMeta, Arparma
from arclet.alconna.graia.dispatcher import AlconnaDispatcher
from graiax.shortcut.saya import listen, dispatch

channel = Channel.current()
channel.name("发病")
channel.description("生成发病(发癫)文字, Eg: .发病")
ill = Alconna(
    ".发病",
    Args["content", [str, At], Empty],
    meta=CommandMeta("生成一段发病文字 Example: .发病 老公;"),
)

with open("./source/ill/data.json", "r", encoding="UTF-8") as f:
    TEMPLATES = json.loads(f.read())["data"]


@listen(GroupMessage)
@dispatch(AlconnaDispatcher(ill, send_flag="reply"))
async def fabing(app: Ariadne, member: Member, group: Group, result: Arparma):
    if result.main_args["content"]:
        content = result.main_args["content"]
        if type(content) == At:
            obj = await app.get_member(group, content.target)
            target = obj.name
        elif type(content) == str:
            target = content
        else:
            return

        if len(target) >= 25:
            await app.send_group_message(group, MessageChain("字数太长啦,想整活?门都没有,封禁了"))
            return
        elif len(target) >= 15:
            await app.send_group_message(group, MessageChain("字数太长啦,谁名字这么长呢"))
            return
    else:
        target = member.name
    await app.send_group_message(
        group, MessageChain(random.choice(TEMPLATES).format(target=target))
    )
