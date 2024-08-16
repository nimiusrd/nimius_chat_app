class ChatCompletion:
    def create_comment(self, query: str | None = None):
        raise NotImplementedError("create_comment is not implemented")

    def create_translation(self, query: str | None = None):
        raise NotImplementedError("create_translation is not implemented")
