# bot.py — aiogram v3 + mistralai — inline с debounce
import logging
import asyncio
from config import settings
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers.main import handlers_router


logging.basicConfig(level=logging.INFO)

async def main() -> None:
    bot = Bot(
        settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="MarkdownV2"),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

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
