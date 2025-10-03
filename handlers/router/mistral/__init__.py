from aiogram import Dispatcher
from . import handler, inline
from aiogram.filters import CommandStart, Command
from aiogram import Router
from filters.WhitelistFilter import WhitelistFilter

import asyncio
from aiogram import types
from client.MistralClient import MistralClient

def prepare_router() -> Router:
    mistral_router = Router()
    mistral_router.message.filter(WhitelistFilter())

    # mistral_router.message.register(handler.handle_text)
    mistral_router.include_router(inline.router)



    return mistral_router



