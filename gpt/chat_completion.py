from openai import OpenAI

from config import config

client = OpenAI(api_key=config.openai.api_key)

from gpt.prompt.sonic_adventure2 import messages


def create_comment():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    return response.choices[0].message.content
