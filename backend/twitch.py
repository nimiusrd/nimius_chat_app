from chat_completion import chat_completion
from config import config
from logger import twitch_logger
from speech_synthesizer import speaker
from twitchAPI.chat import ChatCommand, ChatMessage, EventData, JoinEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

COMMAND_PREFIX = "!"
COMMANDS = ["gpt"]
BOT_ACCOUNT_LIST = [
    "8hvdes",
    "anotherttvviewer",
    "d0nk7",
    "drapsnatt",
]


async def authenticate():
    twitch = await Twitch(config.twitch.app_id, config.twitch.app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE, url="http://0.0.0.0:8080/login/confirm")
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    return twitch, auth


def is_command(text: str) -> bool:
    return any(text.startswith(f"{COMMAND_PREFIX}{command}") for command in COMMANDS)


async def apply_websocket(websocket):
    async def on_ready(ready_event: EventData):
        twitch_logger.info("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(config.twitch.target_channel)
        comment = chat_completion.create_small_talk()
        await speaker.talk(comment, websocket, True)

    async def on_message(msg: ChatMessage):
        if is_command(msg.text):
            return
        twitch_logger.info("%s said: %s", msg.user.name, msg.text)
        await speaker.talk(msg.text, websocket)
        # translation = chat_completion.create_translation(msg.text)
        # twitch_logger.info("Translation: %s", translation)
        # await msg.reply(f"🤖{translation}")

    async def on_join(event: JoinEvent):
        if event.user_name in BOT_ACCOUNT_LIST:
            return
        twitch_logger.info("Joined channel %s", event.user_name)
        comment = chat_completion.create_greeting(event.user_name)
        await speaker.talk(comment, websocket, True)

    async def create_gpt_comment(cmd: ChatCommand):
        twitch_logger.info("Creating GPT comment")
        query = cmd.parameter
        if query != "":
            await speaker.talk(query, websocket)
        comment = chat_completion.create_comment(query)
        await cmd.send(comment)
        await speaker.talk(comment, websocket, True)
        # translation = chat_completion.create_translation(comment)
        # twitch_logger.info("Translation: %s", translation)
        # await cmd.send(f"🤖{translation}")

    return create_gpt_comment, on_message, on_ready, on_join
