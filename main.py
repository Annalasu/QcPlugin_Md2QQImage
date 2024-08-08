from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import re
import mirai

"""
在收到私聊或群聊消息中包含 Markdown 图片链接时，将其转换为 QQ 支持的图片消息格式并正确显示。
"""

# 注册插件
@register(name="MdLink2Image", description="Convert Markdown image links to QQ image format", version="0.2", author="Annalasu")
class MarkdownImageConverterPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 转换 Markdown 图片链接为 QQ 支持的图片消息格式
    def convert_markdown_image(self, text):
        pattern = re.compile(r'!\[.*?\]\((.*?)\)')
        matches = pattern.findall(text)
        images = []
        for url in matches:
            images.append(mirai.Image(url=url))
        return images

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        images = self.convert_markdown_image(msg)
        if images:
            ctx.add_return("reply", images)
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        images = self.convert_markdown_image(msg)
        if images:
            ctx.add_return("reply", images)
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
