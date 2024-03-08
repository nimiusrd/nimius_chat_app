""" configure logger for the project. """

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

twitch_logger = logging.getLogger("twitch")
voicevox_logger = logging.getLogger("voicevox")
gpt_logger = logging.getLogger("gpt")
