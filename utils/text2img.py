import re
from graiax.text2img.playwright import (
    HTMLRenderer,
    MarkdownConverter,
    PageOption,
    ScreenshotOption,
)
from graiax.text2img.playwright.renderer import BuiltinCSS
from .fonts_provider import fill_font

html_render = HTMLRenderer(
    page_option=PageOption(device_scale_factor=1.5),
    screenshot_option=ScreenshotOption(
        type="jpeg", quality=80, full_page=True, scale="device"
    ),
    css=(
        BuiltinCSS.reset,
        BuiltinCSS.github,
        BuiltinCSS.one_dark,
        BuiltinCSS.container,
        "@font-face{font-family:'harmo';font-weight:300;"
        "src:url('http://static.graiax/fonts/HarmonyOS_Sans_SC_Light.ttf') format('truetype');}"
        "@font-face{font-family:'harmo';font-weight:400;"
        "src:url('http://static.graiax/fonts/HarmonyOS_Sans_SC_Regular.ttf') format('truetype');}"
        "@font-face{font-family:'harmo';font-weight:500;"
        "src:url('http://static.graiax/fonts/HarmonyOS_Sans_SC_Medium.ttf') format('truetype');}"
        "@font-face{font-family:'harmo';font-weight:600;"
        "src:url('http://static.graiax/fonts/HarmonyOS_Sans_SC_Bold.ttf') format('truetype');}"
        "*{font-family:'harmo',sans-serif}",
    ),
    page_modifiers=[
        lambda page: page.route(lambda url: bool(re.match('^http://static.graiax/fonts/(.+)$', url)), fill_font)
    ],
)
md_converter = MarkdownConverter()


async def md2img(text: str, width: int = 800) -> bytes:
    html = md_converter.convert(text)

    return await html_render.render(
        html,
        extra_page_option=PageOption(viewport={"width": width, "height": 10}),
    )
