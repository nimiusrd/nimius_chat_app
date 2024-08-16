from chat_completion.base import ChatCompletion
from chat_completion.gemini import GeminiChatCompletion
from chat_completion.openai import OpenaiChatCompletion
from config import GEMINI, OPENAI, config

chat_completion: ChatCompletion

if config.generative_ai == OPENAI:
    chat_completion = OpenaiChatCompletion()
elif config.generative_ai == GEMINI:
    chat_completion = GeminiChatCompletion()
else:
    raise ValueError("Invalid chat completion provider.")
