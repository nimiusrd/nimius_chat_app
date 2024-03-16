from config import config

# from gpt.prompt import mbon as prompt
from gpt.prompt import sonic_adventure2 as prompt
from logger import gpt_logger
from openai import OpenAI

client = OpenAI(api_key=config.openai.api_key)


def create_comment(query: str | None = None):
    gpt_logger.info("Loading messages.")
    messages = prompt.messages
    gpt_logger.info("Messages loaded.")
    gpt_logger.info("Creating chat completion.")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=(
            messages
            if query == "" or query is None
            else [
                messages[0],
                {
                    "role": "user",
                    "content": f"""次の質問に100文字以内で回答してください。${query}""",
                },
            ]
        ),
        temperature=1,
    )
    gpt_logger.info("Chat completion created.")

    return response.choices[0].message.content


if __name__ == "__main__":
    import sys

    print(create_comment(sys.argv[1] if len(sys.argv) > 1 else None))
