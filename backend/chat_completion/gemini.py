import google.generativeai as genai
from chat_completion.base import ChatCompletion
from config import config
from logger import chat_completion_logger


def create_prompt(query: str, prompt: str):
    result = prompt.replace("{{query}}", query)
    return result


class GeminiChatCompletion(ChatCompletion):
    model: str
    temperature: float

    def __init__(self, model: str = "gemini-1.5-flash", temperature: float = 1.0):
        genai.configure(api_key=config.gemini.api_key)
        self.client = genai.GenerativeModel(model)
        self.temperature = temperature

    def create_comment(self, query: str | None = None):
        chat_completion_logger.info("Creating chat completion.")
        response = self.client.generate_content(
            create_prompt(
                query,
                """
あなたはゲーム配信者のアシスタントです。
ゲーム配信者の視聴者は配信者のことに関するコメントをします。
あなたはそのコメントに対して反応してください。

#[反応のルール]
必ず絵文字を使うようにしてください。
60文字以内になるようにしてください。

#[ゲーム配信者の視聴者のコメント]
「{{query}}」
""",
            )
        )
        chat_completion_logger.info("Chat completion created.")
        return response.text

    def create_greeting(self, query: str | None = None):
        chat_completion_logger.info("Creating chat completion.")
        response = self.client.generate_content(
            create_prompt(
                query,
                """
あなたはゲーム配信者のアシスタントです。
ゲーム配信者の視聴者は配信者のことに関するコメントをします。
あなたは視聴者に対して挨拶をしてください。

#[挨拶のルール]
必ず絵文字を使うようにしてください。
60文字以内になるようにしてください。
視聴者の名前は「{{query}}」です。
視聴者の名前には敬称をつけてください。
視聴者の気を引くような一言を添えてください。
出力は1つだけです。
""",
            )
        )
        chat_completion_logger.info("Chat completion created.")
        return response.text
