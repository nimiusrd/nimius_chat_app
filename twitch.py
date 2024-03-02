from twitchAPI.chat import ChatMessage, ChatSub, EventData

from config import config
from logger import twitch_logger
from voicevox import talk


async def on_ready(ready_event: EventData):
    twitch_logger.info("Bot is ready for work, joining channels")
    await ready_event.chat.join_room(config.twitch.target_channel)
    talk("準備完了しました。")


async def on_message(msg: ChatMessage):
    twitch_logger.info("%s said: %s", msg.user.name, msg.text)
    talk(msg.text)
