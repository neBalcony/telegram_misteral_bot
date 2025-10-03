from aiogram import types

async def reply(message: types.Message):
    await message.reply(f"Your *msg* **msg**: {message.text}")