import tomllib
from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    api_key: str


@dataclass
class TwitchConfig:
    app_id: str
    app_secret: str
    target_channel: str


@dataclass
class VOICEVOXConfig:
    speaker: int
    url: str
    output: str = "dist/output.wav"


@dataclass
class Config:
    twitch: TwitchConfig
    voicevox: VOICEVOXConfig
    openai: OpenAIConfig


def read_config():
    with open("config.toml", "rb") as f:
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
            output=voicevox.get("output", "dist/output.wav"),
        ),
        openai=OpenAIConfig(api_key=openai["api_key"]),
    )


config = read_config()

if __name__ == "__main__":
    print(read_config())
