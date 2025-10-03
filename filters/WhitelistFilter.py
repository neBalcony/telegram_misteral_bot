import logging
from config import settings
from aiogram.filters import BaseFilter

class WhitelistFilter(BaseFilter):
    admin_ids = settings.ADMIN_ID
    """
    Фильтр, который разрешает выполнение хэндлера только если
    user_id или chat_id есть в белом списке. Админы всегда разрешены.
    """
    def __init__(self):
        pass

    async def __call__(self, obj) -> bool:
        logging.warning(f"Checking access for user {obj.from_user.id}")
        logging.warning(f"Admin {self.admin_ids}")
        """
        obj — может быть types.Message или types.InlineQuery (aiogram передаёт объект)
        возвращает True если доступ разрешён, False — если нет
        """
        # всегда разрешаем администраторам
        uid = obj.from_user.id
        if uid in self.admin_ids:
            return True
        #TODO Add access for specific usernames
        if obj.from_user.username == "":
            return True

        return False
