import asyncio
from aiogram import Router, types
from mistralai import SystemMessage, UserMessage
from client.MistralClient import MistralClient
from aiogram.exceptions import TelegramBadRequest
import telegramify_markdown
from config import settings
from filters import WhitelistFilter
from db import SessionLocal
from sqlalchemy.sql import select
from models import User

#instruction
router = Router()

@router.message(WhitelistFilter())
async def handle_text(message: types.Message):
    with SessionLocal() as session:
        user = session.execute(select(User).where(User.id == message.from_user.id)).scalars().first()
        if user:
            default_request = user.default_request
    user_text = (message.text or "").strip()
    if not user_text:
        await message.reply("Похоже, пустое сообщение. Попробуйте ещё раз.")
        return

    sending = await message.reply("Отправляю запрос в модель\\.\\.\\. ⏳")
    mistral_msg = []
    if default_request:
        mistral_msg.append(SystemMessage(content=default_request))
    mistral_msg.append(UserMessage(content=user_text))
    
    try:
        MISTRAL_MODEL = settings.MISTRAL_MODEL
        async with MistralClient() as mistral:
            resp = await mistral.chat.complete_async( model=MISTRAL_MODEL, messages=mistral_msg)
            
        assistant_text = ""
        try:
            assistant_text = resp.choices[0].message.content
        except Exception:
            try:
                assistant_text = resp.choices[0].content
            except Exception:
                assistant_text = str(resp)

        converted = telegramify_markdown.markdownify(
            assistant_text,
            max_line_length=None,  # If you want to change the max line length for links, images, set it to the desired value.
            normalize_whitespace=False
        )

        await sending.edit_text(converted)
    except TelegramBadRequest as e:
        if "can't parse" in str(e):
            error_text=f"Ошибка при форматирований {str (e)}\nОтвет модели:\n{converted}"
            await sending.edit_text(error_text,parse_mode=None)
        else:
            await sending.edit_text(f"Ошибка Telegram: {e}", parse_mode=None)

    except Exception as e:
        await sending.edit_text(f"Ошибка при запросе к Mistral: {e}", parse_mode=None)
        
