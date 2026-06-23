from modules.rag.modules.application import RAGApplication


if __name__ == "__main__":
    app = RAGApplication()
    print(app.answer("hello", documents=["test File"]))
