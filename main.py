import asyncio

from twitchAPI.chat import Chat, ChatMessage, ChatSub, EventData
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent

from config import config
from voicevox import talk

USER_SCOPE = [AuthScope.CHAT_READ]


async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    await ready_event.chat.join_room(config.twitch.target_channel)


async def on_message(msg: ChatMessage):
    print(f"{msg.user.name} said: {msg.text}")
    talk(msg.text)


async def on_sub(sub: ChatSub):
    print(
        f"New subscription in {sub.room.name}:\\n"
        f"  Type: {sub.sub_plan}\\n"
        f"  Message: {sub.sub_message}"
    )


async def run():
    twitch = await Twitch(config.twitch.app_id, config.twitch.app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.SUB, on_sub)

    chat.start()

    try:
        input("press ENTER to stop\\n")
    finally:
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())
