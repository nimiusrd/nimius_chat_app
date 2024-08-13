from typing import Annotated

from config import config
from fastapi import FastAPI, Query, WebSocket, WebSocketException, status
from fastapi.responses import RedirectResponse
from logger import socket_logger, twitch_logger
from twitch import USER_SCOPE, apply_websocket
from twitchAPI.chat import Chat
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import ChatEvent, TwitchAPIException

app = FastAPI()
twitch: Twitch
auth: UserAuthenticator


@app.get("/health")
async def health():
    return "ok"


@app.get("/login")
async def login():
    await twitch_setup()
    return RedirectResponse(auth.return_auth_url())


@app.websocket("/")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    code: Annotated[str | None, Query()] = None,
    state: Annotated[str | None, Query()] = None,
):
    await websocket.accept()
    if code is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    if state is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    if auth is None or state != auth.state:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    try:
        token, refresh = await auth.authenticate(user_token=code)
    except TwitchAPIException as e:
        twitch_logger.error("Failed to generate auth token: %s", e)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION) from e
    await twitch.set_user_authentication(token, USER_SCOPE, refresh)
    chat = await Chat(twitch)

    create_gpt_comment, on_message, on_ready, on_join = await apply_websocket(websocket)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.JOIN, on_join)
    chat.register_command("gpt", create_gpt_comment)

    twitch_logger.info("Starting chat")
    chat.start()

    try:
        while True:
            data = await websocket.receive_text()
            socket_logger.info(data)
            await websocket.send_text(f"Message text was: {data}")
    finally:
        twitch_logger.info("Closing chat")
        chat.stop()
        await twitch.close()


async def twitch_setup():
    global twitch, auth
    twitch = await Twitch(config.twitch.app_id, config.twitch.app_secret)
    auth = UserAuthenticator(twitch, USER_SCOPE, url=config.twitch.frontend_url)
