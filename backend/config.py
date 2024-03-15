""" Configuration for OpenAI, Twitch, VOICEVOX API. You can get the configuration from `config.toml`."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


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


@dataclass
class VOICEVOXConfig:
    """Configuration for VOICEVOX API.

    Parameters
    ----------
    speaker : int
        Speaker ID. You can get it from http://localhost:50021/speakers.

    url : str
        VOICEVOX API URL.

    output : str
        Output file path for synthesized voice.
    """

    speaker: int
    url: str
    output: str = "dist/output.wav"


@dataclass
class Config:
    """Configuration for OpenAI, Twitch, VOICEVOX API."""

    twitch: TwitchConfig
    voicevox: VOICEVOXConfig
    openai: OpenAIConfig


def read_config():
    """Read configuration from `config.toml`."""

    with Path("config.toml").open("rb") as f:
        data = tomllib.load(f)
    twitch = data["twitch"]
    voicevox = data["voicevox"]
    openai = data["openai"]
    return Config(
        twitch=TwitchConfig(
            app_id=twitch["app_id"],
            app_secret=twitch["app_secret"],
            target_channel=twitch["target_channel"],
        ),
        voicevox=VOICEVOXConfig(
            speaker=voicevox["speaker"],
            url=f'http://{voicevox.get("host", "localhost")}:{voicevox.get("port", 50021)}',
            output=voicevox.get("output", "frontend/public/output.wav"),
        ),
        openai=OpenAIConfig(api_key=openai["api_key"]),
    )


config = read_config()

if __name__ == "__main__":
    print(read_config())
