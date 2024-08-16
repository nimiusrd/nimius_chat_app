""" Configuration for OpenAI, Twitch, VOICEVOX API. You can get the configuration from `config.toml`."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal

CLOUD_TEXT_TO_SPEECH: Final = "cloud_text_to_speech"
VOICEVOX: Final = "voicevox"
OPENAI: Final = "openai"
GEMINI: Final = "gemini"


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI API.

    Parameters
    ----------
    api_key : str
        OpenAI API Key. You can get it from https://platform.openai.com/account/api-keys.
    """

    api_key: str


@dataclass
class GeminiConfig:
    """Configuration for Gemini API.

    Parameters
    ----------
    api_key : str
        Gemini API Key. You can get it from https://aistudio.google.com/app/apikey.
    """

    api_key: str


@dataclass
class TwitchConfig:
    """Configuration for Twitch API.s

    Parameters
    ----------
    app_id : str
        Twitch Application ID. You can get it from https://dev.twitch.tv/console/apps.
    app_secret : str
        Twitch Application Secret. You can get it from https://dev.twitch.tv/console/apps.
    target_channel : str
        Target channel name.
    """

    app_id: str
    app_secret: str
    target_channel: str
    frontend_url: str


@dataclass
class VOICEVOXConfig:
    """Configuration for VOICEVOX API.

    Parameters
    ----------
    speaker : int
        Speaker ID. You can get it from http://localhost:50021/speakers.

    bot_speaker : int
        Bot speaker ID. You can get it from http://localhost:50021/speakers.
        If you don't set bot speaker ID, use speaker ID.

    url : str
        VOICEVOX API URL.

    output : str
        Output file path for synthesized voice.
    """

    speaker: int
    bot_speaker: int
    url: str
    output: str = "dist/output.wav"


@dataclass
class Config:
    """Configuration for OpenAI, Twitch, VOICEVOX API."""

    twitch: TwitchConfig
    voicevox: VOICEVOXConfig
    openai: OpenAIConfig
    gemini: GeminiConfig
    speech_synthesizer: Literal["cloud_text_to_speech", "voicevox"]
    generative_ai: Literal["openai", "gemini"]


def read_config():
    """Read configuration from `config.toml`."""

    with Path("config.toml").open("rb") as f:
        data = tomllib.load(f)
    twitch = data["twitch"]
    voicevox = data["voicevox"]
    openai = data["openai"]
    gemini = data["gemini"]
    return Config(
        twitch=TwitchConfig(
            app_id=twitch["app_id"],
            app_secret=twitch["app_secret"],
            target_channel=twitch["target_channel"],
            frontend_url=twitch["frontend_url"],
        ),
        voicevox=VOICEVOXConfig(
            speaker=voicevox["speaker"],
            bot_speaker=voicevox.get("bot_speaker", voicevox["speaker"]),
            url=f'http://{voicevox.get("host", "localhost")}:{voicevox.get("port", 50021)}',
            output=voicevox.get("output", "frontend/public/output.wav"),
        ),
        openai=OpenAIConfig(api_key=openai["api_key"]),
        gemini=GeminiConfig(api_key=gemini["api_key"]),
        speech_synthesizer=data["speech_synthesizer"],
        generative_ai=data["generative_ai"],
    )


config = read_config()

if __name__ == "__main__":
    print(read_config())
