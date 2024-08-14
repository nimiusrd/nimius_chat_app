from fastapi.websockets import WebSocket
from logger import speech_synthesizer_logger


class Speaker:
    async def talk(self, text: str, websocket: WebSocket, is_bot: bool = False) -> None:
        speech_synthesizer_logger.info("Talking to '%s'", text)

        if (content := self._synthesize(text, is_bot)) is None:
            speech_synthesizer_logger.error("Failed to talk to '%s'", text)
            return
        if is_bot:
            try:
                await websocket.send_text(text)
            except Exception as e:
                speech_synthesizer_logger.error("Failed to send text to websocket. %s", e)
        try:
            await websocket.send_bytes(content)
        except Exception as e:
            speech_synthesizer_logger.error("Failed to send audio to websocket. %s", e)
        speech_synthesizer_logger.info("Successfully talked to '%s'", text)

    def _synthesize(self, text: str, is_bot: bool) -> bytes | None:
        raise NotImplementedError()
