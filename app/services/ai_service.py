import os
import logging
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_service")

class OpenRouterService:
    """Сервис для взаимодействия с OpenRouter API."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = 30  # Таймаут в секундах

        if not self.api_key:
            logger.error("OPENROUTER_API_KEY не найден в переменных окружения (.env)")
            raise ValueError("Missing OPENROUTER_API_KEY in environment variables")

    def send_message(self, messages: list, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Отправляет сообщение в OpenRouter API и возвращает ответ в формате JSON.
        
        :param messages: Список сообщений в формате [{'role': 'user', 'content': '...'}]
        :param system_prompt: Опциональный системный промпт для задания поведения бота
        :return: Словарь с ответом или ошибкой
        """
        # Добавляем системный промпт, если он указан и его еще нет в истории
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000", # Обязательно для OpenRouter
            "X-Title": "Developer Portfolio Bot",      # Обязательно для OpenRouter
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
        }

        try:
            logger.info(f"Sending request to OpenRouter using model: {self.model}")
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=self.timeout
            )
            
            # Вызывает HTTPError если статус код 4xx или 5xx
            response.raise_for_status()
            
            result = response.json()
            
            # Извлекаем текст сообщения из структуры ответа OpenRouter/OpenAI
            answer = result['choices'][0]['message']['content']
            
            logger.info("Request successfully processed by OpenRouter")
            return {
                "status": "success",
                "answer": answer,
                "model": self.model
            }

        except requests.exceptions.Timeout:
            logger.error("Request to OpenRouter API timed out")
            return {"status": "error", "message": "Request timeout. Please try again later."}
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return {"status": "error", "message": f"API Error: {e.response.status_code}"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected error during request: {str(e)}")
            return {"status": "error", "message": "An unexpected error occurred while contacting AI service."}
            
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected response structure from API: {str(e)}")
            return {"status": "error", "message": "Invalid response format from AI service."}

# Синглтон для использования в приложении
ai_service = OpenRouterService()
