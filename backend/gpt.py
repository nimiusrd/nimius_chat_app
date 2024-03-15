import sys

from gpt.chat_completion import create_comment

if __name__ == "__main__":
    print(create_comment(sys.argv[1] if len(sys.argv) > 1 else None))
