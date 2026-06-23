from llm_service import llm_service

def test_lmstudio():
    print("Тестируем подключение к LM Studio...")

    try:
        response = llm_service.generate(
            prompt="Привет, как дела?",
            system_prompt="Ты дружелюбный помощник."
        )

        print("Ответ от LM Studio:", {response})
        print("Тест подключения к LM Studio прошел успешно.")

    except Exception as e:
        print("Ошибка при тестировании подключения к LM Studio:", {e})


if __name__ == "__main__":
    test_lmstudio()