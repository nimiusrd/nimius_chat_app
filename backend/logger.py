""" configure logger for the project. """

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

twitch_logger = logging.getLogger("twitch")
speech_synthesizer_logger = logging.getLogger("speech_synthesizer")
chat_completion_logger = logging.getLogger("gpt")
socket_logger = logging.getLogger("socket")
