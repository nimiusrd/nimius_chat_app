import winsound

import requests

from config import config
from gui import app
from logger import voicevox_logger


def play_by_gui():
    def play():
        winsound.PlaySound(config.voicevox.output, winsound.SND_FILENAME)

    app.after(0, play)


def talk(text):
    voicevox_logger.info("Talking to '%s", text)
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

    with open(config.voicevox.output, "wb") as f:
        f.write(synthesis.content)

    voicevox_logger.debug("synthesis status: %d", synthesis.status_code)

    play_by_gui()

    voicevox_logger.info("Successfully talked to '%s'", text)


if __name__ == "__main__":
    talk("こんにちは、私はボイスボックスです。")
