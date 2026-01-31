from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from filters.chat_filters import ChatTypeFilter

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
            types.KeyboardButton(text="Information about bot...")
        ],
        [
            types.KeyboardButton(text="How use the bot?")
        ],
        [
            types.KeyboardButton(text="View all commands")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True, 
        input_field_placeholder='Select an option'
    )
    await message.answer(text, reply_markup=keyboard)

@user_private_router.message(F.text.lower() == 'information about bot...')
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    text = (
        "<b>🛡️ Professional Moderation Service</b>\n\n"
        "I am designed to act as a silent guardian for your chat. By utilizing a robust "
        "keyword filtering system and <b>persistent storage (SQLAlchemy 2.0)</b>, I identify "
        "and manage violations in real-time.\n\n"
        "<b>Core Capabilities:</b>\n"
        "• <i>Persistent Tracking</i>: All warnings and mutes are saved in a database.\n"
        "• <i>Real-time Scanning</i> of all messages and edits.\n"
        "• <i>Automated Warning System</i> to educate users before taking action.\n"
        "• <i>Progressive Mutes</i>: Intelligent scaling of restrictions (up to several days).\n"
        "• <i>Manual Moderation</i>: Admins can use /warn, /mute, or /ban.\n\n"
        "I respect your administrators and ensure they retain full control while I handle "
        "the routine moderation tasks."
    )
    await message.reply(text)

@user_private_router.message(F.text.lower() == 'how use the bot?')
@user_private_router.message(Command("how_use_bot"))
async def how_to_use_cmd(message: types.Message):
    text = (
        "<b>⚙️ Configuration Instructions</b>\n\n"
        "Follow these steps to enable protection in your group:\n\n"
        "1. <b>Add the Bot</b> to your group chat.\n"
        "2. <b>Promote to Administrator</b> and ensure <i>Delete Messages</i> and "
        "<i>Ban Users</i> permissions are enabled.\n"
        "3. <b>Supergroup Activation</b>: Confirm your chat is a Supergroup to allow "
        "me to restrict members.\n\n"
        "Once configured, you can use commands by <b>replying</b> to messages or by providing a <b>User ID</b>."
    )
    await message.reply(text)

@user_private_router.message(F.text.lower() == 'view all commands')
@user_private_router.message(Command("help"))
async def commands_cmd(message: types.Message):
    text = (
        "<b>📜 Available Commands</b>\n\n"
        "<b>Group Administration:</b>\n"
        "• /mute <code>[time/ID] [set]</code> - Mute user (reply or ID required).\n"
        "• /unmute - Unmute user (reply required).\n"
        "• /ban <code>[time/ID] [set]</code> - Ban user (reply or ID required).\n"
        "• /unban <code>[ID]</code> - Unban user (reply or ID required).\n\n"
        "<b>Time Formats:</b>\n"
        "<code>10m</code>, <code>1h</code>, <code>1d</code>, <code>1w</code>, <code>permanent</code>\n\n"
        "<b>Arguments:</b>\n"
        "• <code>set</code> - Use this to update or extend the duration for a user who is already restricted.\n\n"
        "<b>Usage Note:</b> Admin commands require the bot to have 'Ban Users' privileges."
    )
    await message.reply(text)
