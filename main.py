import asyncio
from tkinter import Tk

from twitchAPI.chat import Chat
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import ChannelStreamScheduleSegment, Twitch
from twitchAPI.type import AuthScope, ChatEvent

from config import config
from gui import app
from logger import twitch_logger
from twitch import create_gpt_comment, on_message, on_ready

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


async def run():
    twitch = await Twitch(config.twitch.app_id, config.twitch.app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command("gpt", create_gpt_comment)

    twitch_logger.info("Starting chat")
    chat.start()

    try:
        input("")
    finally:
        twitch_logger.info("Closing chat")
        chat.stop()
        await twitch.close()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    app.after(0, main)
    app.mainloop()
