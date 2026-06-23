from inbox_agent import InBoxAgent

def test_inbox_agent():
    print("Тестируем InBoxAgent...")
    print("-" * 50)

subject = "Вопрос по налогам"
body = """
Здравствуйте!
    
    Я получил счет №12345 от 15 ноября 2024 года на сумму 50 000 рублей.
    Подскажите, пожалуйста, до какого числа я должен оплатить этот счет?
    
    С уважением,
    Иван Петров
"""

print(f"Тема письма: {subject}")
print(f"Текст письма: {body}")
print("-" * 50)

print("Определяем категорию письма...")
classification = InBoxAgent().classify_email(subject, body)
print("Результат классификации:", classification)
print("-" * 50)

print("Генерируем черновик ответа...")
draft = InBoxAgent().generate_draft_response(
    subject,
    body,
    category=classification.get("category", "general_question")
)
print(f"📝 Черновик ответа:\n{draft}")
print("-" * 50)

if __name__ == "__main__":
    test_inbox_agent()