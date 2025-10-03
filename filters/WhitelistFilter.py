from aiogram.filters import BaseFilter
from typing import Union
from aiogram import types
from filters.AdminFilter import AdminFilter


class WhitelistFilter(BaseFilter):
    users_id = []
    usernames = []  # добавим для имен

    def __init__(self):
        self.admin_filter = AdminFilter()

    async def __call__(self, obj: Union[types.Message, types.CallbackQuery, types.InlineQuery]) -> bool:
        # проверяем админа через AdminFilter
        if await self.admin_filter(obj):
            return True

        # проверяем по id
        if obj.from_user.id in WhitelistFilter.users_id:
            return True

        # проверяем по username (если указано)
        if obj.from_user.username and obj.from_user.username in WhitelistFilter.usernames:
            return True

        # если ничего не подошло — доступ запрещён
        return False

    @classmethod
    def add_user(cls, uid: int):
        if uid not in cls.users_id:
            cls.users_id.append(uid)

    @classmethod
    def add_username(cls, username: str):
        if username not in cls.usernames:
            cls.usernames.append(username)

    @classmethod
    def is_user_in_whitelist(cls, uid: int) -> bool:
        if uid == AdminFilter.admin_id:
            return True
        return uid in cls.users_id
