import asyncio

import websockets
from logger import socket_logger, twitch_logger
from twitch import apply_websocket, authenticate
from twitchAPI.chat import Chat
from twitchAPI.type import ChatEvent
from websockets import WebSocketServerProtocol


async def handler(websocket: WebSocketServerProtocol) -> None:
    socket_logger.info("Connected to client")
    twitch = await authenticate()
    chat = await Chat(twitch)

    create_gpt_comment, on_message, on_ready, on_join = await apply_websocket(websocket)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_event(ChatEvent.JOIN, on_join)
    chat.register_command("gpt", create_gpt_comment)

    twitch_logger.info("Starting chat")
    chat.start()

    try:
        async for message in websocket:
            socket_logger.info(message)
    finally:
        twitch_logger.info("Closing chat")
        chat.stop()
        await twitch.close()


async def main():
    async with websockets.serve(handler, "localhost", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
