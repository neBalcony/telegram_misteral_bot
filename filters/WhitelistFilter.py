from typing import Union
from aiogram import types
from sqlalchemy import select
from filters.AdminFilter import AdminFilter
from aiogram.filters import BaseFilter
from models import User,UserRole
from db import SessionLocal



class WhitelistFilter(BaseFilter):

    async def __call__(self, obj: Union[types.Message, types.CallbackQuery, types.InlineQuery]) -> bool:
        uid = obj.from_user.id
        return self.is_user_in_whitelist(uid)

    #TODO: Move to crud.py
    @classmethod
    def add_user(cls, uid: int, role: UserRole):
        with SessionLocal() as session:
            user = User(id=uid, role=role)
            session.add(user)
            session.commit()

    #TODO: Move to crud.py
    @classmethod
    def is_user_in_whitelist(cls, uid: int) -> bool:
        with SessionLocal() as session:
            user = session.execute(select(User).where(User.id == uid)).scalars().first()
            
            # Проверяем есть ли user
            if user:
                return True
            return False