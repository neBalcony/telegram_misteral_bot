# example for aiogram v3
from aiogram.filters import Command
from aiogram import Router
from . import get_id, reply


def prepare_router():
    util_router = Router()

    # register the handler with the Command filter
    util_router.message.register(get_id.get_id, Command(commands=["get_id"]))
    util_router.message.register(reply.reply, Command(commands=["reply"]))
    return util_router
