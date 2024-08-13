""" configure logger for the project. """

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

twitch_logger = logging.getLogger("twitch")
speech_synthesizer_logger = logging.getLogger("speech_synthesizer")
gpt_logger = logging.getLogger("gpt")
socket_logger = logging.getLogger("socket")
