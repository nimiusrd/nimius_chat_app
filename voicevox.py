import requests

from config import config
from logger import voicevox_logger


async def talk(text, websocket):
    voicevox_logger.info("Talking to '%s'", text)
    try:
        query = requests.post(
            f"{config.voicevox.url}/audio_query",
            params={"text": text, "speaker": config.voicevox.speaker},
            timeout=1000,
        )

        voicevox_logger.debug("query status: %d", query.status_code)

        synthesis = requests.post(
            f"{config.voicevox.url}/synthesis",
            params={"speaker": config.voicevox.speaker},
            data=query.content,
            timeout=1000,
        )

        voicevox_logger.debug("synthesis status: %d", synthesis.status_code)

        await websocket.send(synthesis.content)

        voicevox_logger.info("Successfully talked to '%s'", text)
    except:
        voicevox_logger.error("Failed to talk to '%s'", text)


# if __name__ == "__main__":
#     talk("こんにちは、私はボイスボックスです。")
