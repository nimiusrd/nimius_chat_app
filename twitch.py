from twitchAPI.chat import ChatCommand, ChatMessage, EventData

from config import config
from gpt.chat_completion import create_comment
from logger import twitch_logger
from voicevox import talk

COMMAND_PREFIX = "!"
COMMANDS = ["gpt"]


def is_command(text: str) -> bool:
    return any(text.startswith(f"{COMMAND_PREFIX}{command}") for command in COMMANDS)


async def on_ready(ready_event: EventData):
    twitch_logger.info("Bot is ready for work, joining channels")
    await ready_event.chat.join_room(config.twitch.target_channel)
    talk("準備完了しました。")


async def on_message(msg: ChatMessage):
    if is_command(msg.text):
        return
    twitch_logger.info("%s said: %s", msg.user.name, msg.text)
    talk(msg.text)


async def create_gpt_comment(cmd: ChatCommand):
    twitch_logger.info("Creating GPT comment")
    query = cmd.parameter
    comment = create_comment(query)
    await cmd.send(f"[gpt]{comment}")
    talk(comment)
