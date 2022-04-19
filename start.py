"""
Demoed by Haphaistos2333(liu.tong1@outlook.com). 2022. All rights reserved.
NOT FOR RELEASE. DO NOT DISTRIBUTE.
"""

from typing import Optional
import asyncio
import wechaty
from wechaty_puppet import MessageType


class DemoMuxBot(wechaty.Wechaty):
    """
    """
    SWITCH_KEYWORD = "Switch bot"

    def __init__(self, options: Optional[wechaty.WechatyOptions] = None):
        super().__init__(options)

    def switch_bot(self, user_id: str, bot: str):
        print(f'{user_id=}, {bot=}')

    async def on_message(self, msg: wechaty.Message) -> None:
        if (msg.message_type == MessageType.MESSAGE_TYPE_TEXT and
                str(msg).startswith(self.SWITCH_KEYWORD)):
            self.switch_bot(
                msg.talker().get_id(),
                str(msg)[len(self.SWITCH_KEYWORD) + 1:].strip()  # 裁掉命令关键字
            )


if __name__ == '__main__':
    class DummyMessage:
        class DummyTalker:
            def __init__(self, user_id: str):
                self.user_id = user_id

            def get_id(self) -> str:
                return self.user_id

        def __init__(self, user_id: str, text: str):
            self.user_id = user_id
            self.payload = text
            self.message_type = MessageType.MESSAGE_TYPE_TEXT

        def __str__(self) -> str:
            return self.payload

        def talker(self) -> DummyTalker:
            return self.DummyTalker(self.user_id)


    bot = DemoMuxBot()  # 这个Bot就是最终start那个
    # 先用IO简单模拟下
    while True:
        print('\n===============')
        user_id = input('输入userid: ')
        msg_text = input('输入消息发送: ')
        msg = DummyMessage(user_id, msg_text)
        asyncio.run(bot.on_message(msg))
