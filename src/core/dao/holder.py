from sqlalchemy.ext.asyncio import AsyncSession

from .rdb import UserDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = UserDAO(self.session)

    async def commit(self):
        await self.session.commit()
