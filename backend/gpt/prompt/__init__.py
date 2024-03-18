from dataclasses import dataclass

from openai.types.chat import ChatCompletionMessageParam


@dataclass
class GPTPrompt:
    messages: list[ChatCompletionMessageParam]
    temperature: float
    model: str = "gpt-3.5-turbo"

    def create_message(self, query: str | None) -> list[ChatCompletionMessageParam]:
        if query == "" or query is None:
            return self.messages
        return [
            *self.messages[:-1],
            {
                "role": "user",
                "content": f"""次の質問に200文字以内で回答してください。${query}""",
            },
        ]
