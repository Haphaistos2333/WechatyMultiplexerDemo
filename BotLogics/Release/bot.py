"""
Demoed by Haphaistos2333(liu.tong1@outlook.com). 2022. All rights reserved.
NOT FOR RELEASE. DO NOT DISTRIBUTE.
Bot执行逻辑
"""
import wechaty


class BotRelease(wechaty.Wechaty):
    async def on_message(self, msg: wechaty.Message) -> None:
        print(f'Bot release received msg: {str(msg)}')
