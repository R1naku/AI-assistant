import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LMStudioService:
    def __init__(self):
        self.base_url = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
        self.model = "qwen"
        self.timeout = 60.0

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        try:
            url = f"{self.base_url}/chat/completions"
            
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": prompt
            })

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 500,
                "stream": False
            }
            
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

            data = response.json()
            
            if "choices" not in data or len(data["choices"]) == 0:
                raise Exception("Некорректный ответ от LM Studio")
            
            return data["choices"][0]["message"]["content"]

        except requests.Timeout:
            return "Ошибка: таймаут при обращении к LM Studio"
        except Exception as e:
            print(f"Ошибка при обращении к LM Studio: {e}")
            return f"Произошла ошибка: {str(e)}"

# Создаем глобальный экземпляр
llm_service = LMStudioService()