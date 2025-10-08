from aiogram import Bot, Router, types
from aiogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from filters import WhitelistFilter
from filters import AdminFilter
from filters import InlineCommand
router = Router()

@router.inline_query(InlineCommand(commands=["/start", "/help"]))
async def inline_command_handler(query: types.InlineQuery, command: str, args: str):
    await query.answer(
        results=[
            InlineQueryResultArticle(
                id="_",
                title="Команда: {command}, аргументы: {args}",
                input_message_content=InputTextMessageContent(
                    message_text="Тут ничего нет ☹️"
                ),
                description=f"Это тестовая функция, которая не делает ничего",
            )
        ],
    )


@router.inline_query(InlineCommand(commands=["/invite"]),AdminFilter())
async def inline_command_handler(query: types.InlineQuery, command: str, args: str):
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Принять ✅",
                callback_data="invite_accept"
            ),
            InlineKeyboardButton(
                text="Отклонить ❌",
                callback_data="invite_decline"
            )
        ]
    ]
    )    
    
    await query.answer(
        results=[InlineQueryResultArticle(
            id="_",
            title="Отправить приглашения",
            input_message_content=InputTextMessageContent(
                message_text="Вам пришло приглашение"
            ),
            reply_markup=keyboard
        )],
    )


@router.callback_query(lambda c: c.data == "invite_accept")
async def invite_accept_handler(callback: CallbackQuery, bot:Bot):
    inline_id = callback.inline_message_id
    if WhitelistFilter.is_user_in_whitelist(callback.from_user.id):
        await bot.edit_message_text(
            inline_message_id=inline_id,
            text=f"Вы уже в белом списке ✅",
            parse_mode=None
        )
        return

    WhitelistFilter.add_user(callback.from_user.id)
    await bot.edit_message_text(
        inline_message_id=inline_id,
        text=f"Приглашение принято ✅",
        parse_mode=None
    )

@router.callback_query(lambda c: c.data == "invite_decline")
async def invite_decline_handler(callback: CallbackQuery, bot:Bot):
    inline_id = callback.inline_message_id
    if WhitelistFilter.is_user_in_whitelist(callback.from_user.id):
        await bot.edit_message_text(
            inline_message_id=inline_id,
            text=f"Но вы уже в белом списке 🙃",
            parse_mode=None
        )
        return

    WhitelistFilter.add_user(callback.from_user.id)
    await bot.edit_message_text(
        inline_message_id=inline_id,
        text=f"Приглашение отклонено ❌",
        parse_mode=None
    )