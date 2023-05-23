from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.core.dao.holder import HolderDao


class InitMiddleware(BaseMiddleware):
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],) -> Any:
        async with self.session() as session:
            holder_dao = HolderDao(session=session)
            data['dao'] = holder_dao
            result = await handler(event, data)
            del data['dao']
        return result
