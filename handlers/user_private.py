from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    text = (
        f"Greetings, <b>{message.from_user.full_name}</b>. I am a specialized moderation bot "
        f"dedicated to keeping your Telegram communities clean and respectful. 🛡️\n\n"
        f"<i>My primary objective is to monitor and filter prohibited content automatically, "
        f"allowing you to focus on meaningful discussions.</i>\n\n"
        f"Use the buttons below to learn more about my features or how to set me up."
    )
    kb = [
        [
            types.KeyboardButton(text="About bot...")
        ],
        [
            types.KeyboardButton(text="How use the bot?")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True, 
        input_field_placeholder='Select an option'
    )
    await message.answer(text, reply_markup=keyboard)

@user_private_router.message(F.text.lower() == 'about bot...')
async def about_cmd(message: types.Message):
    text = (
        "<b>🛡️ Professional Moderation Service</b>\n\n"
        "I am designed to act as a silent guardian for your chat. By utilizing a robust "
        "keyword filtering system, I identify and manage profanity in real-time.\n\n"
        "<b>Core Capabilities:</b>\n"
        "• <i>Real-time Scanning</i> of all messages and edits.\n"
        "• <i>Automated Warning System</i> to educate users before taking action.\n"
        "• <i>Temporary Restrictions</i> (1 hour) for repeat violators to maintain order.\n\n"
        "I respect your administrators and ensure they retain full control while I handle "
        "the routine moderation tasks."
    )
    await message.reply(text)

@user_private_router.message(F.text.lower() == 'how use the bot?')
async def how_to_use_cmd(message: types.Message):
    text = (
        "<b>⚙️ Configuration Instructions</b>\n\n"
        "Follow these steps to enable protection in your group:\n\n"
        "1. <b>Add the Bot</b> to your group chat.\n"
        "2. <b>Promote to Administrator</b> and ensure <i>Delete Messages</i> and "
        "<i>Ban Users</i> permissions are enabled.\n"
        "3. <b>Supergroup Activation</b>: Confirm your chat is a Supergroup to allow "
        "me to restrict members.\n\n"
        "Once these steps are complete, I will immediately begin my watch. 🛡️"
    )
    await message.reply(text)