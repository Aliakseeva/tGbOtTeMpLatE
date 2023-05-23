from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ManagerMiddleware(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any], ) -> Any:
        data['bot'] = self.bot
        return await handler(event, data)
