from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from config.strings import ABOUT_TEXT, COMMANDS_TEXT, CONFIG_TEXT, KB_ALL_COMMANDS, KB_HOW_USE_BOT, KB_INFO_BOT, WELCOME_TEXT_PRIVATE
from filters.chat_filters import ChatTypeFilter
from loguru import logger

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    """
    Handler for the /start command in private messages.
    Provides a welcome message and navigation keyboard.
    """
    logger.info(f"User {message.from_user.id} started bot in private")
    
    text = WELCOME_TEXT_PRIVATE.format(full_name=message.from_user.full_name)
    kb = [
        [types.KeyboardButton(text=KB_INFO_BOT)],
        [types.KeyboardButton(text=KB_HOW_USE_BOT)],
        [types.KeyboardButton(text=KB_ALL_COMMANDS)],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Select an option"
    )
    await message.answer(text, reply_markup=keyboard)


@user_private_router.message(F.text.lower() == "information about bot...")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    """
    Handler for the /about command or information button.
    Displays technical details and bot capabilities.
    """
    await message.reply(text=ABOUT_TEXT)


@user_private_router.message(F.text.lower() == "how use the bot?")
@user_private_router.message(Command("how_use_bot"))
async def how_to_use_cmd(message: types.Message):
    """
    Handler for the setup instructions command or button.
    Provides step-by-step configuration guide.
    """
    await message.reply(text=CONFIG_TEXT)


@user_private_router.message(F.text.lower() == "view all commands")
@user_private_router.message(Command("help"))
async def commands_cmd(message: types.Message):
    """
    Handler for the /help command or view commands button.
    Lists all available commands and their usage.
    """
    await message.reply(text=COMMANDS_TEXT)
