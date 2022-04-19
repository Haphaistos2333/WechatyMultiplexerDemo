"""
Demoed by Haphaistos2333(liu.tong1@outlook.com). 2022. All rights reserved.
NOT FOR RELEASE. DO NOT DISTRIBUTE.
Bot切换框架
"""
from typing import Optional
import asyncio
from importlib import import_module
from collections import defaultdict
import wechaty
from wechaty_puppet import MessageType


class DemoMuxBot(wechaty.Wechaty):
    """
    """
    SWITCH_KEYWORD = 'Switch bot'
    RELEASE_BOT = 'Release'  # Release是BotLogics下当前线上版本的包名，也是默认回复的Bot。TODO: 这个是必须存在的，启动时可以校验下

    def __init__(self, options: Optional[wechaty.WechatyOptions] = None):
        super().__init__(options)

        def get_default_logic():
            """封一个闭包丢给defaultdict，防止重复执行import操作"""
            bot = import_module(f'BotLogics.{self.RELEASE_BOT}').LogicBot()
            return lambda: bot

        self.logic_bot_map = defaultdict(get_default_logic())

    def switch_bot(self, user_id: str, bot: str):
        print(f'Switching to {bot}...')
        try:
            bot_module = import_module(f'BotLogics.{bot}')
        except ModuleNotFoundError:
            print('Error: Module not found')
            return
        self.logic_bot_map[user_id] = bot_module.LogicBot()
        print('Done')

    async def on_message(self, msg: wechaty.Message) -> None:
        talker_id = msg.talker().get_id()
        # TODO: 校验检查还可以判一下是不是有权限的管理员
        if (msg.message_type == MessageType.MESSAGE_TYPE_TEXT and
                str(msg).startswith(self.SWITCH_KEYWORD)):
            self.switch_bot(
                talker_id,
                str(msg)[len(self.SWITCH_KEYWORD) + 1:].strip()  # 裁掉命令关键字
            )
            return
        return await self.logic_bot_map[talker_id].on_message(msg)


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
