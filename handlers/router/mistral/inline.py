import asyncio
import logging
from uuid import uuid4
from mistralai import SystemMessage, UserMessage
import redis
from sqlalchemy import select
import telegramify_markdown
from telegramify_markdown import ContentTypes, InterpreterChain, TextInterpreter
from aiogram.filters.callback_data import CallbackData
from aiogram import Bot, Router
from aiogram.types import (
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from mistralai.models import SDKError
from client.MistralClient import MistralClient
from db import SessionLocal
from filters import WhitelistFilter
from config import settings
from models import User

MISTRAL_MODEL = settings.MISTRAL_MODEL

class QstData(CallbackData, prefix="qst_"): #TODO: move to separate file
    qst_uuid: str

router = Router()
logging.basicConfig(level=logging.INFO)



@router.inline_query(WhitelistFilter())
async def inline_handler(inline_query: InlineQuery):
    uuid = uuid4()
    id_str = str(uuid)
    query_text = (inline_query.query or "").strip()

    if not query_text:
        me = await inline_query.bot.get_me()
        result = InlineQueryResultArticle(
            id="_",
            title="Задайте вопрос Mistral.ai",
            input_message_content=InputTextMessageContent(
                message_text="Введите вопрос в строку выше и выберите этот пункт"
            ),
            description=f"Бот: @{me.username}",
        )
        await inline_query.answer([result])
        return
    r_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    ONE_WEEK = 60*60*24*7
    r_client.set(id_str, query_text, ex=ONE_WEEK)
    r_client.close()
    kb = InlineKeyboardMarkup(inline_keyboard = [
        [
            InlineKeyboardButton(text="Получит ответ",callback_data=QstData(qst_uuid=id_str).pack())
            ]
        ]) 
    result = InlineQueryResultArticle(
        id=id_str,
        title=f"Вопрос:{query_text}",
        input_message_content=InputTextMessageContent(message_text=f"Вопрос:{query_text}", parse_mode=None),
        reply_markup=kb
    )

    await inline_query.answer([result],cache_time=0)


def get_inline_kb_retry(data):
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Попробовать ещё",
                callback_data=data  # тут можно свой хендлер на колбэк
            )
        ]
    ]
    )
    return keyboard


#TODO: REFACTOR
@router.callback_query(QstData.filter())
async def callback_edit_handler(callback: CallbackQuery, bot: Bot):
    try:
        # Подтверждаем нажатие (чтобы пользователь видел ответ)
        uuid = QstData.unpack(callback.data).qst_uuid
        r_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        question = r_client.get(uuid)
        r_client.close()
        if question is None:
            logging.warning("Question for uuid %s not found (maybe already processed or expired)", uuid)
            # дружелюбно сообщаем пользователю
            await callback.answer("Вопрос устарел или уже обработан.", show_alert=True)
            return
        await callback.answer("Понял принял, жди ответа...", show_alert=False)

        # qst_id.pop(uuid, None)

        # callback.inline_message_id присутствует для inline-сообщений
        inline_id = callback.inline_message_id

        if inline_id:
            # редактируем по inline_message_id
            # bot.edit_message_text(inline_id, text="Сообщение изменено")
            try:
                await bot.edit_message_text(inline_message_id=inline_id, text="Запрашиваю ответ у модели\\.\\.\\. ⏳")
            except Exception as e:
                logging.error(f"Error editing message: {e} try again")
                await bot.edit_message_text(inline_message_id=inline_id, text="Запрашиваю ответ у модели\\.\\.\\. ⏳")
                
            with SessionLocal() as session:
                user = session.execute(select(User).where(User.id == callback.from_user.id)).scalars().first()
                default_request = user.default_request
            mistral_msg = []
            if default_request:
                mistral_msg.append(SystemMessage(content=default_request))
            mistral_msg.append(UserMessage(content=question))

            
            mistral = MistralClient.get_mistral()
            def call_mistral():
                return mistral.chat.complete(model=MISTRAL_MODEL, messages=mistral_msg)
            try:

                resp = await asyncio.to_thread(call_mistral)
            except SDKError as e:
                logging.error(f"Error calling Mistral API: {e}")


                await bot.edit_message_text(
                    inline_message_id=inline_id,
                    text=f"Ошибка при получении ответа от модели.\nВопрос: {question}",
                    reply_markup=get_inline_kb_retry(callback.data),
                    parse_mode=None
                )
                return
            assistant_text = ""
            try:
                assistant_text = resp.choices[0].message.content
            except Exception:
                logging.warning("resp.choices[0].message.content rise error, trying resp.choices[0].content")
                try:
                    assistant_text = resp.choices[0].content
                except Exception:
                    logging.warning("resp.choices[0].content raise error, trying str(resp)")
                    assistant_text = str(resp)


            boxs = await telegramify_markdown.telegramify(
            content=assistant_text,
                interpreters_use=InterpreterChain([TextInterpreter()]),
                latex_escape=True,
                normalize_whitespace=True,
                max_word_count=4090  # The maximum number of words in a single message.
            )
            if boxs[0].content_type == ContentTypes.TEXT:
                converted = boxs[0].content
            else:
                logging.error("First box is not text, using fallback message")
                converted = "Что то пошло не так при обработке ответа от модели.☹️ Простите"

            try:
                
                await bot.edit_message_text(inline_message_id=inline_id, text=converted)
            except Exception as e:
                logging.error(f"Error editing message: {e}")
                await bot.edit_message_text(inline_message_id=inline_id, 
                                            text="Что то пошло не так при обработке ответа от модели.☹️ Простите", 
                                            parse_mode=None,
                                            reply_markup=get_inline_kb_retry(callback.data),
                                        )
    except Exception as e:
        logging.error(f"Unexpected error in callback handler: {e}")
        try:
            if callback.inline_message_id:
                await bot.edit_message_text(
                    inline_message_id=callback.inline_message_id,
                    text="⚠ Ошибка при обработке запроса",
                    parse_mode=None
                )

        except Exception as e2:
            logging.error(f"Failed to notify user about error: {e2}")
            raise e2

#TODO REFACTOR WHOLE FILE