import asyncio
from aiogram import types
from client.MistralClient import MistralClient
from aiogram.exceptions import TelegramBadRequest
import telegramify_markdown
from config import settings

#instruction

async def handle_text(message: types.Message):
    #TODO: Сделать DI
    mistral = MistralClient.get_mistral()
    MISTRAL_MODEL = settings.MISTRAL_MODEL
    
    
    # не обрабатываем команды здесь
    if message.text and message.text.startswith("/"):
        return

    user_text = (message.text or "").strip()
    if not user_text:
        await message.reply("Похоже, пустое сообщение. Попробуйте ещё раз.")
        return


    sending = await message.reply("Отправляю запрос в модель\\.\\.\\. ⏳")
    mistral_msg = []
    mistral_msg.append({                     
            "role": "user",
            "content": user_text,
        })
    
    try:
        def call_mistral():
            return mistral.chat.complete(
                model=MISTRAL_MODEL,
                messages=mistral_msg)

        resp = await asyncio.to_thread(call_mistral)

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
            await sending.edit_text(f"Ошибка Telegram: {e}",)

    except Exception as e:
        await sending.edit_text(f"Ошибка при запросе к Mistral: {e}",)
        
