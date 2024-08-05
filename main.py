from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
import re
import mirai


@register(name="Md2QQImage", description="Convert Markdown images to QQ images", version="0.1",
          author="Annalasu")
class MarkdownImagePlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.host = host

    async def initialize(self):
        pass

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        converted_message = self.convert_markdown_to_qq_message(msg)
        if converted_message:
            await ctx.reply(converted_message)
            ctx.prevent_default()

    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        converted_message = self.convert_markdown_to_qq_message(msg)
        if converted_message:
            await ctx.reply(converted_message)
            ctx.prevent_default()

    def convert_markdown_to_qq_message(self, markdown_message: str):
        markdown_image_pattern = r'!\[.*?\]\((.*?)\)'
        image_urls = re.findall(markdown_image_pattern, markdown_message)
        if not image_urls:
            return None

        qq_message_chain = mirai.MessageChain()
        for url in image_urls:
            qq_message_chain.append(mirai.Image.from_url(url))

        return qq_message_chain

    def __del__(self):
        pass
