from aiogram.filters import BaseFilter
from aiogram.types import Message


class CustomFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return True
