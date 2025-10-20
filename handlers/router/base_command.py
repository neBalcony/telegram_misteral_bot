from aiogram.filters import CommandStart, Command, CommandObject
from aiogram import Router
from aiogram import types
from aiogram.utils.formatting import Text
from aiogram import types

from filters import AdminFilter


router = Router()




@router.message(Command("invite"),AdminFilter())
async def invite_username(message, command: CommandObject):
    
    args = command.args
    if "@" in args:
        args = args.replace("@","")
    if len(args.split(" "))>1:
        pass
    
    await message.reply(message)
    
@router.message(CommandStart())
async def start(message: types.Message):
    text = (
        "Привет! Я бот, который использует Mistral.ai.\n"
        "Вы можете писать мне в личку или использовать меня в inline-режиме — введите @<мой_ник> в любом чате.\n"
        "Команды:\n"
        "/help — это сообщение"
    )
    content = Text(text) 
    
    await message.reply(**content.as_kwargs())


@router.message(Command("help"))
async def help(message: types.Message):
    text = (
        "Я бот, который использует Mistral.ai.\n"
        "Вы можете писать мне в личку или использовать меня в inline-режиме — введите @<мой_ник> в любом чате.\n"
        "Команды:\n"
        "/start — приветственное сообщение\n"
        "/help — это сообщение"
    )
    content = Text(text) 
    
    await message.reply(**content.as_kwargs())


