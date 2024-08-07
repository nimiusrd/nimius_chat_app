import requests
from config import config
from logger import speech_synthesizer_logger
from speech_synthesizer.base import Speaker


class VoicevoxSpeaker(Speaker):
    def __init__(self):
        pass

    def _synthesize(self, text: str, is_bot: bool) -> bytes | None:
        try:
            query = requests.post(
                f"{config.voicevox.url}/audio_query",
                params={"text": text, "speaker": config.voicevox.bot_speaker if is_bot else config.voicevox.speaker},
                timeout=1000,
            )
        except Exception as e:
            speech_synthesizer_logger.error("Failed to create audio query. %s", e)
            return None
        speech_synthesizer_logger.debug("query status: %d", query.status_code)
        try:
            synthesis = requests.post(
                f"{config.voicevox.url}/synthesis",
                params={"speaker": config.voicevox.bot_speaker if is_bot else config.voicevox.speaker},
                data=query.content,
                timeout=1000,
            )
        except Exception as e:
            speech_synthesizer_logger.error("Failed to synthesize audio. %s", e)
            return None
        speech_synthesizer_logger.debug("synthesis status: %d", synthesis.status_code)

        return synthesis.content
