from config import config
from gpt.chat_completion import create_comment, create_translation
from logger import twitch_logger
from twitchAPI.chat import ChatCommand, ChatMessage, EventData, JoinEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope
from voicevox import talk

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

COMMAND_PREFIX = "!"
COMMANDS = ["gpt"]


async def authenticate():
    twitch = await Twitch(config.twitch.app_id, config.twitch.app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    return twitch


def is_command(text: str) -> bool:
    return any(text.startswith(f"{COMMAND_PREFIX}{command}") for command in COMMANDS)


async def apply_websocket(websocket):
    async def on_ready(ready_event: EventData):
        twitch_logger.info("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(config.twitch.target_channel)
        await talk("準備完了しました。", websocket, True)

    async def on_message(msg: ChatMessage):
        if is_command(msg.text):
            return
        twitch_logger.info("%s said: %s", msg.user.name, msg.text)
        await talk(msg.text, websocket)
        translation = create_translation(msg.text)
        twitch_logger.info("Translation: %s", translation)
        await msg.reply(f"🤖{translation}")

    async def on_join(event: JoinEvent):
        twitch_logger.info("Joined channel %s", event.user_name)

    async def create_gpt_comment(cmd: ChatCommand):
        twitch_logger.info("Creating GPT comment")
        query = cmd.parameter
        if query != "":
            await talk(query, websocket)
        comment = create_comment(query)
        await cmd.send(comment)
        await talk(comment, websocket, True)
        translation = create_translation(comment)
        twitch_logger.info("Translation: %s", translation)
        await cmd.send(f"🤖{translation}")

    return create_gpt_comment, on_message, on_ready, on_join
