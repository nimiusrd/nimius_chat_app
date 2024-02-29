import winsound

import requests

from config import config


def talk(text):
    print(f"Talking to '{text}'")
    query = requests.post(
        f"{config.voicevox.url}/audio_query",
        params={"text": text, "speaker": config.voicevox.speaker},
        timeout=1000,
    )

    print(f"query status: {query.status_code}")

    synthesis = requests.post(
        f"{config.voicevox.url}/synthesis",
        params={"speaker": config.voicevox.speaker},
        data=query.content,
        timeout=1000,
    )

    print(f"synthesis status: {synthesis.status_code}")

    winsound.PlaySound(synthesis.content, winsound.SND_MEMORY)


if __name__ == "__main__":
    talk("こんにちは")
