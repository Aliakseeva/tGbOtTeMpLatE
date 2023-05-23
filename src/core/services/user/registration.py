from aiogram.types import Message
from src.core.dao.holder import HolderDao


async def start_user(message: Message, dao: HolderDao):
    id_ = message.from_user.id
    user = await dao.user.get_user_by_id(id_=id_)
    if user:
        return user

    user_data = {
        'id_': message.from_user.id,
        'role': 'user',
        'locale': message.from_user.language_code
    }

    await dao.user.add_user(user_data)
    await dao.commit()
    return await start_user(message, dao)
