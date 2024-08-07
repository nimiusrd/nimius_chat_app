from config import CLOUD_TEXT_TO_SPEECH, VOICEVOX, config
from speech_synthesizer.cloud_text_to_speech import CloudTextToSpeechSpeaker
from speech_synthesizer.voicevox import VoicevoxSpeaker

speaker: VoicevoxSpeaker | CloudTextToSpeechSpeaker

if config.speech_synthesizer == VOICEVOX:
    speaker = VoicevoxSpeaker()
elif config.speech_synthesizer == CLOUD_TEXT_TO_SPEECH:
    speaker = CloudTextToSpeechSpeaker()
else:
    raise ValueError("Invalid speech synthesizer")
