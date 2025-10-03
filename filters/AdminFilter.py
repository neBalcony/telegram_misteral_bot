from config import settings
from aiogram.filters import BaseFilter
from typing import Union
from aiogram import types

class AdminFilter(BaseFilter):
    admin_id = settings.ADMIN_ID

    async def __call__(self, obj: Union[types.Message, types.CallbackQuery, types.InlineQuery]) -> bool:
        return obj.from_user.id == self.admin_id

