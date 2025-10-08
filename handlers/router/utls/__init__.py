from aiogram import Router
from aiogram.filters import Command
from . import get_id, reply

util_router = Router()
util_router.message.register(get_id.get_id, Command(commands=["get_id"]))
util_router.message.register(reply.reply, Command(commands=["reply"]))