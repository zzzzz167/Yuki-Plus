import aiohttp


async def getAvatar(qqunm: int) -> bytes:
    async with aiohttp.request(
        "GET", "https://q2.qlogo.cn/headimg_dl?dst_uin=%s&spec=640" % str(qqunm)
    ) as resp:
        return await resp.read()
