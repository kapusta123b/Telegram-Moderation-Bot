import asyncio
import os

from dotenv import load_dotenv
load_dotenv(".env.prod")  # delete '.prod' if you want use bot token

from database.engine import create_db, session_maker
from middlewares.db import DbSessionMiddleware

from handlers.user_group import user_group_router
from handlers.user_private import user_private_router

from bot_cmd_list import user_private_commands, admin_group_commands

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types


ALLOWED_UPDATES = ["message", "edited_message", "my_chat_member", "chat_member", "callback_query"]

bot = Bot(
    token=os.environ.get('SECRET_KEY'),  # write your secret token in .env file
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(user_group_router)

async def main():
    await create_db()

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=user_private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=admin_group_commands, scope=types.BotCommandScopeAllChatAdministrators())
    
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())