# bot.py — aiogram v3 + mistralai — inline с debounce
import logging


# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Handler для DEBUG и INFO
info_handler = logging.FileHandler('info.log', encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.addFilter(lambda record: record.levelno <= logging.INFO)  # только DEBUG и INFO
info_handler.setFormatter(formatter)

# Handler для WARNING
warning_handler = logging.FileHandler('warning.log', encoding='utf-8')
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(lambda record: record.levelno == logging.WARNING)
warning_handler.setFormatter(formatter)

# Handler для ERROR и CRITICAL
error_handler = logging.FileHandler('error.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавляем обработчики в root logger
logging.basicConfig(level=logging.INFO, handlers=[info_handler, warning_handler, error_handler, console_handler])

import asyncio
from config import settings
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers.main import handlers_router
from middelware import UpdateUserMiddleware




async def main() -> None:
    bot = Bot(
        settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="MarkdownV2"),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.middleware(UpdateUserMiddleware())
# Register routs
    dp.include_router(handlers_router)
    
    try:
        await dp.start_polling(bot)
    finally:
        try:
            await bot.session.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
