from chat_completion.base import ChatCompletion
from chat_completion.prompt.gbvsr import prompt

# from .prompt.mbon import prompt
from chat_completion.prompt.translation import prompt as translation
from config import config
from logger import chat_completion_logger
from openai import OpenAI


class OpenaiChatCompletion(ChatCompletion):
    model: str
    temperature: float

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 1.0):
        self.client = OpenAI(api_key=config.openai.api_key)
        self.temperature = temperature
        self.model = model

    def create_comment(self, query: str | None = None):
        chat_completion_logger.info("Creating chat completion.")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt.create_message(query),
            temperature=self.temperature,
        )
        chat_completion_logger.info("Chat completion created.")

        return response.choices[0].message.content

    def create_translation(self, query: str | None = None):
        chat_completion_logger.info("Creating chat completion.")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=translation.create_message(query),
            temperature=self.temperature,
        )
        chat_completion_logger.info("Chat completion created.")

        return response.choices[0].message.content
