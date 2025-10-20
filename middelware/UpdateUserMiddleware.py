from typing import Any, Callable
from aiogram import types
from aiogram import BaseMiddleware,types
from db import SessionLocal
from models import Invite, User, UserRole
    
class UpdateUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Any, data: dict):
        # event — например types.Message или types.CallbackQuery
        # Получаем объект пользователя (если есть)
        user_obj = None
        if isinstance(event, types.Update):
            user_obj = event.event.from_user

        if user_obj:
            username = getattr(user_obj, "username", None)
            if username:
                # Работа с синхронной SQLAlchemy (SessionLocal — sync)
                with SessionLocal() as session:
                    invite = session.query(Invite).filter(Invite.username == username).first()
                    if invite:
                        # Лучше использовать merge, чтобы не вставлять дубликат с тем же PK
                        user = User(id=user_obj.id, username=username, role = UserRole.user)
                        session.merge(user)   # merge безопаснее, обновит/вставит
                        session.delete(invite)
                        session.commit()

        # продолжить обработку апдейта
        return await handler(event, data)