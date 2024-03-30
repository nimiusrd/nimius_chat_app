from config import config
from gpt.prompt.mameda_no_bakeru import prompt

# from gpt.prompt.mbon import prompt
from gpt.prompt.translation import prompt as translation
from logger import gpt_logger
from openai import OpenAI

client = OpenAI(api_key=config.openai.api_key)


def create_comment(query: str | None = None):
    gpt_logger.info("Creating chat completion.")
    response = client.chat.completions.create(
        model=prompt.model,
        messages=prompt.create_message(query),
        temperature=prompt.temperature,
    )
    gpt_logger.info("Chat completion created.")

    return response.choices[0].message.content


def create_translation(query: str | None = None):
    gpt_logger.info("Creating chat completion.")
    response = client.chat.completions.create(
        model=prompt.model,
        messages=translation.create_message(query),
        temperature=translation.temperature,
    )
    gpt_logger.info("Chat completion created.")

    return response.choices[0].message.content


if __name__ == "__main__":
    import sys

    print(create_comment(sys.argv[1] if len(sys.argv) > 1 else None))
