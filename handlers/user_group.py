from pathlib import Path
from string import punctuation
from aiogram import Bot, types, Router
from datetime import datetime, timedelta
from filters.chat_types import ChatTypeFilter




user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))


BAD_WORDS_FILE = Path(__file__).parent / "banwords.txt"

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    BAD_WORDS = {line.strip().lower() for line in f if line.strip()}

users = {}

def normalize(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation)).lower()

def contains_bad_word(text: str) -> bool:
    normalized = normalize(text)
    words = normalized.split()

    if BAD_WORDS.intersection(words):
        return True

    for bad_word in BAD_WORDS:
        if bad_word in normalized:
            return True

    return False

@user_group_router.edited_message
@user_group_router.message()
async def cleaner(message: types.Message, bot: Bot):
    if not message.text:
        return

    if not contains_bad_word(message.text):
        return

    user_id = message.from_user.id
    first_name = message.from_user.first_name

    warnings = users.get(user_id, 0) + 1
    users[user_id] = warnings

    member = await bot.get_chat_member(message.chat.id, user_id)
    if member.status in ("creator", "administrator"):
        await message.answer("⚠️ <b>Admin Notice:</b> Please maintain professional language.", parse_mode="HTML")
        return

    if warnings < 3:
        await message.answer(
            f"⚠️ <b>Warning {warnings}/3:</b> {first_name}, prohibited language is not allowed.",
            parse_mode="HTML"
        )
        await message.delete()
        return

    users[user_id] = 0

    permissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
    )

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        permissions=permissions,
        until_date=datetime.now() + timedelta(minutes=60),
    )

    await message.answer(
        text=f"🚫 <b>User Restricted:</b> {first_name} reached <b>3/3</b> warnings.\n<i>1-hour restriction applied.</i>",
        parse_mode="HTML"
    )
    await message.delete()


@user_group_router.my_chat_member()
async def on_bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator"):
        await event.answer(
            "🛡 <b>Profanity Filter Bot</b>\n\n"
            "I will automatically monitor this chat for prohibited language. "
            "Users receive warnings, and after <b>3/3</b> warnings, they are restricted for 1 hour.\n\n"
            "<b>Setup:</b>\n"
            "To function properly, I need administrator rights:\n"
            "1. Open Group Settings > <b>Administrators</b>\n"
            "2. Add me as an admin\n"
            "3. Enable <b>Delete Messages</b> and <b>Ban Users</b> permissions",
            parse_mode="HTML"
        )
