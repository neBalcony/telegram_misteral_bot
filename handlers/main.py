from aiogram import Router
from .router import base_command, mistral,utls

mistral_router = mistral.prepare_router()
utls_router = utls.prepare_router()


handlers_router = Router()

handlers_router.include_router(mistral_router)
handlers_router.include_router(utls_router)
handlers_router.include_router(base_command.router)
