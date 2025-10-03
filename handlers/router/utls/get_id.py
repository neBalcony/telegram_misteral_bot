from aiogram import types

async def get_id(message: types.Message):
    await message.answer(f"Your id: {message.from_user.id}")