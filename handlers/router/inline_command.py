from aiogram import Bot, Router, types
from aiogram.types import (
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from mistralai.models import SDKError
from client.MistralClient import MistralClient
from filters.WhitelistFilter import WhitelistFilter
from filters.InlineCommand import InlineCommand
from config import settings

router = Router()

@router.inline_query(InlineCommand(commands=["/start", "/help"]))
async def inline_command_handler(query: types.InlineQuery, command: str, args: str, bot: Bot):
    me = await query.bot.get_me()
    await query.answer(
        results=[],
        switch_pm_text=f"Команда: {command}, аргументы: {args}, Это тестовая функция, которая не делает ничего",
        switch_pm_parameter="1"
    )


@router.inline_query(InlineCommand())
async def inline_command_handler(query: types.InlineQuery, command: str, args: str, bot: Bot):
    me = await query.bot.get_me()
    await query.answer(
        results=[InlineQueryResultArticle(
            id="_",
            title="Отправить команду11",
            input_message_content=InputTextMessageContent(
                message_text="Введите вопрос в строку выше и выберите этот пункт"
            ),
            description=f"Бот: @{me.username}",
        )],        
        switch_pm_text=f"Команда: {command}, аргументы: {args}, Это тестовая функция, которая не делает ничего",

        switch_pm_parameter="1"
    )
