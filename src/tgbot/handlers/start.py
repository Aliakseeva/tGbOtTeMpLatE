from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.core.dao.holder import HolderDao
from src.core.services.user.registration import start_user


router = Router()


@router.message(Command("start"))
async def cmd_user_start(message: Message, dao: HolderDao, i18n):
    user = await start_user(message=message, dao=dao)
    text = i18n.user.start(username=message.from_user.username, user=user.__str__())

    commands = [i18n.help(),
                i18n.back()]

    builder = ReplyKeyboardBuilder()
    for c in commands:
        builder.add(KeyboardButton(text=c))

    await message.answer(text=text, reply_markup=builder.as_markup(resize_keyboard=True))
