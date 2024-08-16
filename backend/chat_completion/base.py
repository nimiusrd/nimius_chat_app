class ChatCompletion:
    def create_comment(self, query: str | None = None):
        raise NotImplementedError("create_comment is not implemented")

    def create_greeting(self, query: str | None = None):
        raise NotImplementedError("create_greeting is not implemented")

    def create_small_talk(self, query: str | None = None):
        raise NotImplementedError("create_small_talk is not implemented")

    def create_translation(self, query: str | None = None):
        raise NotImplementedError("create_translation is not implemented")
