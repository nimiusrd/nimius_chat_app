from google.cloud import texttospeech
from speech_synthesizer.base import Speaker


class CloudTextToSpeechSpeaker(Speaker):
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def _synthesize(self, text: str, is_bot: bool) -> bytes | None:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
