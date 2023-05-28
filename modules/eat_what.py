import random
from aiofile import async_open
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Source
from graia.saya import Channel
from arclet.alconna import Alconna
from arclet.alconna.graia.dispatcher import AlconnaDispatcher
from graiax.shortcut.saya import dispatch, listen

channel = Channel.current()
channel.name("今天吃什么")
channel.description("随机挑选干饭材料")
eatALC = Alconna('.吃啥')


async def get_food():
    async with async_open('./source/eat_what/foods.txt') as afp:
        foods = await afp.read()
    return random.choice(foods.strip().split('\n'))


@listen(GroupMessage)
@dispatch(AlconnaDispatcher(eatALC, send_flag="reply"))
async def main(app: Ariadne, group: Group, source: Source):
    food = await get_food()
    chain = MessageChain(Plain(f'吃{food}'))
    await app.send_message(group, chain, quote=source)
