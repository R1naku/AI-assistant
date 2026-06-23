from llm_service import llm_service
from typing import Dict, Any
import json
import re


class InBoxAgent:
    def __init__(self):
        self.classification_prompt = """
Ты - агент по обработке входящих писем для бухгалтерской/юридической фирмы.
Твоя задача - классифицировать входящие письма по категориям.

Категории:
1. "invoice" - счета, инвойсы, финансовые документы
2. "consultation_request" - запросы на консультацию
3. "general_question" - общие вопросы
4. "complaint" - жалобы, проблемы
5. "other" - всё остальное

Отвечай ТОЛЬКО в формате JSON:
{
    "category": "название_категории",
    "confidence": 0.0-1.0,
    "reason": "краткое объяснение почему так решил"
}
"""

        self.draft_system_prompt = """
Ты - ассистент бухгалтера/юриста. Твоя задача - подготовить 
вежливый и профессиональный черновик ответа на письмо клиента.

Правила:
1. Отвечай на том же языке, что и письмо
2. Будь вежливым и профессиональным
3. Если запрос сложный - предложи записаться на консультацию
4. Не давай юридических или финансовых гарантий
5. Подпись: "С уважением, команда поддержки"
"""

    def classify_email(self, subject: str, body: str, sender: str = None, sender_name: str = None) -> Dict[str, Any]:
        sender_info = ""
        if sender:
            sender_info += f"Отправитель: {sender}\n"
        if sender_name:
            sender_info += f"Имя отправителя: {sender_name}\n"
        
        prompt = f"""
{sender_info}
Проанализируй письмо и определи его категорию.

Тема: {subject}
Текст: {body}

Определи категорию и верни JSON.
"""
        
        response = llm_service.generate(
            prompt=prompt,
            system_prompt=self.classification_prompt
        )

        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["sender"] = sender
                result["sender_name"] = sender_name
                return result
            else:
                return {
                    "category": "other",
                    "confidence": 0.5,
                    "reason": "Не удалось распознать JSON в ответе модели",
                    "sender": sender,
                    "sender_name": sender_name
                }
            
        except Exception as e:
            return {   
                "category": "other",
                "confidence": 0.3,
                "reason": f"Ошибка при разборе JSON: {str(e)}",
                "sender": sender,
                "sender_name": sender_name
            }
        
    def generate_draft_response(self, subject: str, body: str, category: str, sender: str = None, sender_name: str = None) -> str:
        greeting = "Здравствуйте!"
        if sender_name:
            greeting = f"Здравствуйте, {sender_name}!"
        elif sender:
            greeting = f"Здравствуйте! (отправитель: {sender})"
        
        prompt = f"""
Клиент написал письмо:
Отправитель: {sender or 'не указан'}
Имя: {sender_name or 'не указано'}
Тема: {subject}
Текст: {body}
Категория: {category}

Подготовь черновик ответа. Начни с обращения: "{greeting}"
"""
        
        response = llm_service.generate(
            prompt=prompt,
            system_prompt=self.draft_system_prompt
        )

        return response


inbox_agent = InBoxAgent()