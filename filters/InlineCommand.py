from aiogram import types
from aiogram.filters import BaseFilter

class InlineCommand(BaseFilter):
    def __init__(self, commands: list[str] | None = None):
        self.commands = commands  # можно ограничить список команд

    async def __call__(self, query: types.InlineQuery) -> dict | bool:
        text = query.query.strip()
        if not text.startswith("/"):
            return False

        command, *args = text.split(maxsplit=1)
        args = args[0] if args else ""

        # Если передали список допустимых команд — проверяем
        if self.commands and command not in self.commands:
            return False

        # Возвращаем данные в хэндлер
        return {
            "command": command,
            "args": args
        }
