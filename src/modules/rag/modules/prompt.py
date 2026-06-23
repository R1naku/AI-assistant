class SystemPrompt:
    def __init__(self):
        self.prompt = (
            "Ты — помощник, отвечающий на вопросы. "
            "Используй только следующий контекст для ответа:\n\n"
            "{context}"
        )


system_prompt = SystemPrompt().prompt


class SimplePromptTemplate:
    def format(self, *, context: str, input: str) -> str:
        return f"{system_prompt}\n\nquestion: {input}\n\ncontext:\n{context}"


prompt = SimplePromptTemplate()