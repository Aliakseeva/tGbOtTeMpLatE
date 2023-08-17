import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.tgbot.config.config import load_config
from src.tgbot.middlewares.db import InitMiddleware
from src.tgbot.middlewares.manager import ManagerMiddleware
from src.tgbot.middlewares.localizator import TranslatorRunnerMiddleware
from src.tgbot.handlers import start, payment
from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle


logger = logging.getLogger(__name__)


def create_pool(db_url, echo):
    engine = create_async_engine(db_url, future=True, echo=echo)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config()

    # Choosing FSM storage
    if config.tg_bot.use_redis:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))
    else:
        dp = Dispatcher(storage=MemoryStorage())

    pool = create_pool(db_url=config.db.DATABASE_URL, echo=False)
    bot = Bot(token=config.tg_bot.bot_token.get_secret_value(), parse_mode='HTML')

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")

    # Register middlewares
    dp.message.middleware(InitMiddleware(pool))
    dp.callback_query.middleware(InitMiddleware(pool))

    dp.message.middleware(ManagerMiddleware(bot))
    dp.callback_query.middleware(ManagerMiddleware(bot))

    dp.message.middleware(TranslatorRunnerMiddleware())
    dp.callback_query.middleware(TranslatorRunnerMiddleware())
    #
    dp.include_routers(start.router, payment.router)

    # Localization tool

    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator("en", translator=FluentBundle.from_files("en", filenames=["src/locales/en.ftl"])),
            FluentTranslator("ru", translator=FluentBundle.from_files("ru", filenames=['src/locales/ru.ftl']))
        ],
    )

    # start
    try:
        # Запускаем бота и пропускаем все накопленные входящие
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, _translator_hub=translator_hub)
    finally:
        await dp.storage.close()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()

