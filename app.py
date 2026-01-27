import asyncio
import os

from aiogram import Bot, Dispatcher, types

from dotenv import load_dotenv
load_dotenv()

from handlers.user_group import user_group_router
from handlers.user_private import user_private_router
from bot_cmd_list import main_menu_commands

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


ALLOWED_UPDATES = ["message", "edited_message", "my_chat_member"]

bot = Bot(
    token=os.environ.get("SECRET_KEY"), # write your secret token in .env file
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
)  

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=main_menu_commands, scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
