from aiogram import Router
from .router import base_command, mistral, utls, inline_command

handlers_router = Router()

handlers_router.include_router(inline_command.router)
handlers_router.include_router(base_command.router)
handlers_router.include_router(mistral.mistral_router)
handlers_router.include_router(utls.util_router)
