from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dao.rdb.base import BaseDAO
from src.core.db.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user_by_id(self, id_: int):
        return await self._get_one_by_id(id_)

    async def get_users_list(self):
        return await self._get_list()

    async def add_user(self, data: dict):
        await self._set_one(obj=User(**data))
        return True
