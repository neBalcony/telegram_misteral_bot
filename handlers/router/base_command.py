from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram import types
from aiogram.utils.formatting import Text
from aiogram import types


router = Router()





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
