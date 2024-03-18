from dataclasses import dataclass

from gpt.prompt import GPTPrompt
from openai.types.chat import ChatCompletionMessageParam


@dataclass
class TranslationGPTPrompt(GPTPrompt):
    def create_message(self, query: str | None) -> list[ChatCompletionMessageParam]:
        if query == "" or query is None:
            raise ValueError("Query must not be empty.")
        return [
            *self.messages,
            {
                "role": "user",
                "content": query,
            },
        ]


prompt = TranslationGPTPrompt(
    messages=[
        {
            "role": "system",
            "content": "あなたは英語か日本語が与えられます。英語ならば日本語に翻訳してください。日本語ならば英語に翻訳してください。",
        },
        {"role": "user", "content": "My name is Jane. What is yours?"},
        {"role": "assistant", "content": "私の名前はジェーンです。あなたの名前は何ですか？"},
        {"role": "user", "content": "こんにちは。私は二郎です。"},
        {"role": "assistant", "content": "Hello. I am Jiro."},
    ],
    temperature=0,
)
