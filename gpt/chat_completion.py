from openai import OpenAI

from config import config
from logger import gpt_logger

client = OpenAI(api_key=config.openai.api_key)

# from gpt.prompt.sonic_adventure2 import messages

import importlib


def create_comment():
    gpt_logger.info("Loading messages.")
    messages = importlib.import_module("gpt.prompt.mbon").messages
    gpt_logger.info("Messages loaded.")
    gpt_logger.info("Creating chat completion.")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    gpt_logger.info("Chat completion created.")

    return response.choices[0].message.content
