import asyncio
import os

from aiogram import Bot, Dispatcher, types

from dotenv import load_dotenv
load_dotenv()

from handlers.user_group import user_group_router


private = [
    types.BotCommand(command='start', description='Start the bot'),
    types.BotCommand(command='help', description='How to use the bot'),
]

ALLOWED_UPDATES = ['message', 'edited_message', 'my_chat_member']

bot = Bot(token=os.environ.get('SECRET_KEY')) # write your secret token in .env file
dp = Dispatcher()

dp.include_router(user_group_router)


async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())