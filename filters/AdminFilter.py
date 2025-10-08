from typing import Union
from aiogram import types
from sqlalchemy import select
from aiogram.filters import BaseFilter
from models import User, UserRole
from db import SessionLocal


class AdminFilter(BaseFilter):

    async def __call__(self, obj: Union[types.Message, types.CallbackQuery, types.InlineQuery]) -> bool:
        with SessionLocal() as session:
            uid = obj.from_user.id 
            user = session.execute(select(User).where(User.id == uid)).scalars().first()
            # If user dont exist
            if not user:
                return False
            
            if user.role is UserRole.admin:
                return True

            # if not admin return false
            return False

