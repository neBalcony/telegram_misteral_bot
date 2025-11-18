from mistralai import Mistral
from config import settings
import asyncio
import logging

class MistralClient():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # инициализация singleton
            cls._instance.lock = asyncio.Lock()
            cls._instance.timeout = settings.MISTRAL_TIMEOUT
            MISTRAL_API_KEY = settings.MISTRAL_API_KEY
            cls._instance.mistral = Mistral(api_key=MISTRAL_API_KEY)

        return cls._instance
    
    async def __aenter__(self):
        await self.lock.acquire()
        return self.mistral
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        def safe_release():
            try:
                if self.lock.locked():
                    self.lock.release()
            except RuntimeError:
                logging.exception("Ошибка при автоматическом освобождении лока")
        
        loop = asyncio.get_running_loop()
        loop.call_later(self.timeout, safe_release)