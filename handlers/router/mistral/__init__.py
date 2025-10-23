from aiogram import Router
from . import handler, inline

mistral_router = Router()
mistral_router.include_router(handler.router)
mistral_router.include_router(inline.router)
