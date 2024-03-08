from openai import OpenAI

from config import config
from logger import gpt_logger

client = OpenAI(api_key=config.openai.api_key)

import importlib

from gpt.prompt import sonic_adventure2 as prompt

# from gpt.prompt import mbon as prompt


def create_comment(query: str | None = None):
    gpt_logger.info("Loading messages.")
    messages = importlib.reload(prompt).messages
    gpt_logger.info("Messages loaded.")
    gpt_logger.info("Creating chat completion.")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=(
            messages
            if query == "" or query is None
            else [
                messages[0],
                {"role": "user", "content": query},
            ]
        ),
        temperature=1,
    )
    gpt_logger.info("Chat completion created.")

    return response.choices[0].message.content
