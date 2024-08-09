from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
import re
from mirai import Image, Plain

@register(name="Md2QQImage", description="优化 bot 发送的消息，将图片链接转换为实际图片", version="1.0", author="Annalasu")
class BotMessageOptimizerPlugin(Plugin):

    def __init__(self, plugin_host: PluginHost):
        super().__init__(plugin_host)
        # 匹配图片 URL 的正则表达式
        self.image_pattern = re.compile(r'\[(https?://\S+)\]')

    @on(NormalMessageResponded)
    def optimize_message(self, event: EventContext, **kwargs):
        original_message = kwargs['response_text']
        optimized_message = self.convert_message(original_message)
        if optimized_message:
            event.add_return('reply', optimized_message)

    def convert_message(self, message):
        parts = []
        last_end = 0
        for match in self.image_pattern.finditer(message):
            start, end = match.span()
            # 添加图片前的文本
            if start > last_end:
                parts.append(Plain(message[last_end:start]))
            # 提取图片 URL 并添加图片
            image_url = match.group(1)
            parts.append(Image(url=image_url))
            parts.append(Plain("[下载]"))  # 添加 [下载] 文本
            last_end = end
        # 添加最后一个图片后的文本
        if last_end < len(message):
            parts.append(Plain(message[last_end:]))
        return parts if parts else message  # 如果没有修改，返回原始消息

    def __del__(self):
        pass