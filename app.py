import asyncio

from os import environ

from dotenv import load_dotenv
load_dotenv(".env")

from config.logging_config import setup_logging
from database.engine import create_db, session_maker
from middlewares.db import DbSessionMiddleware

from handlers.user_group import user_group_router
from handlers.user_private import user_private_router

from config.config import user_private_commands, admin_group_commands, ALLOWED_UPDATES

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types

from loguru import logger

setup_logging()

bot = Bot(
    token=environ.get("SECRET_KEY"), # write your secret token in .env file
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(user_group_router)

async def main():
    await create_db()

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=user_private_commands, scope=types.BotCommandScopeAllPrivateChats()
    )
    await bot.set_my_commands(
        commands=admin_group_commands,
        scope=types.BotCommandScopeAllChatAdministrators(),
    )

    logger.success('Bot successfully started and polling...')
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())