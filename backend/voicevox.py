import requests
from config import config
from logger import voicevox_logger
from websockets import WebSocketServerProtocol


def synthesize(text: str) -> bytes | None:
    try:
        query = requests.post(
            f"{config.voicevox.url}/audio_query",
            params={"text": text, "speaker": config.voicevox.speaker},
            timeout=1000,
        )
    except Exception as e:
        voicevox_logger.error("Failed to create audio query. %s", e)
        return None
    voicevox_logger.debug("query status: %d", query.status_code)
    try:
        synthesis = requests.post(
            f"{config.voicevox.url}/synthesis",
            params={"speaker": config.voicevox.speaker},
            data=query.content,
            timeout=1000,
        )
    except Exception as e:
        voicevox_logger.error("Failed to synthesize audio. %s", e)
        return None
    voicevox_logger.debug("synthesis status: %d", synthesis.status_code)

    return synthesis.content


async def talk(
    text: str, websocket: WebSocketServerProtocol, is_bot: bool = False
) -> None:
    voicevox_logger.info("Talking to '%s'", text)
    if (content := synthesize(text)) is None:
        voicevox_logger.error("Failed to talk to '%s'", text)
        return
    try:
        if is_bot:
            await websocket.send(text)
        await websocket.send(content)
    except Exception as e:
        voicevox_logger.error("Failed to send audio to websocket. %s", e)
    voicevox_logger.info("Successfully talked to '%s'", text)


# if __name__ == "__main__":
#     talk("こんにちは、私はボイスボックスです。")
