from aiogram.filters import CommandStart, Command, CommandObject
from aiogram import Router
from aiogram import types
from aiogram.utils.formatting import Text
from aiogram import types
from sqlalchemy import select

from db import SessionLocal
from models import Invite
from filters import AdminFilter


router = Router()


@router.message(Command("invite"), AdminFilter())
async def invite_username(message, command: CommandObject):
    args = command.args
    if not args:
        await message.reply(
            "Нету имя 🙃\nДолжно быть одно слово: @username", parse_mode=None
        )
        return

    if "@" in args:
        args = args.replace("@", "")

    args = args.strip()
    if len(args.split(" ")) > 1:
        await message.reply(
            "Не валидное имя 🙃\nДолжно быть одно слово: @username", parse_mode=None
        )
        return
    with SessionLocal() as session:
        invite = (
            session.execute(select(Invite).where(Invite.username == args))
            .scalars()
            .first()
        )
        if invite:
            await message.reply(f"Ползователь @{args} уже приглашен", parse_mode=None)
            return

        invite = Invite(username=args)
        session.add(invite)
        session.commit()

    await message.reply(f"Ползователь @{args} приглашен", parse_mode=None)


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

    
