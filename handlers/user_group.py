from pathlib import Path
from string import punctuation
from aiogram import Bot, types, Router
from aiogram.filters import Command
from datetime import datetime, timedelta

from filters.chat_types import ChatTypeFilter
from aiogram.filters.command import CommandObject


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


BAD_WORDS_FILE = Path(__file__).parent / "banwords.txt"

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    BAD_WORDS = {line.strip().lower() for line in f if line.strip()}

users = {}


permissions_mute = types.ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)


permissions_unmute = types.ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


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


def parse_time(time_str: str) -> datetime | str | None:
    if time_str == "permanent":
        return "permanent"
    
    unit = time_str[-1]
    units = {"m": "minutes", "h": "hours", "d": "days", 'w': "weeks"}
    
    if unit not in units:
        return None
        
    try:
        value = int(time_str[:-1])
        return datetime.now() + timedelta(**{units[unit]: value})
    
    except ValueError:
        return None


@user_group_router.message(Command("mute"))
async def mute_cmd(message: types.Message, command: CommandObject, bot: Bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("creator", "administrator"):
        return

    if not command.args:
        await message.reply(
            "❌ <b>Error:</b> Provide duration (e.g., <code>10m</code>, <code>1h</code>, <code>permanent</code>)."
        )
        return

    if not message.reply_to_message:
        await message.reply("❌ <b>Error:</b> Reply to a user's message.")
        return

    user_id = message.reply_to_message.from_user.id
    
    target_member = await bot.get_chat_member(message.chat.id, user_id)
    if target_member.status in ("creator", "administrator"):
        await message.reply("❌ <b>Error:</b> Cannot mute an administrator.")
        return

    time_arg = command.args.split()[0].lower()
    until_date = parse_time(time_arg)

    if until_date is None:
        await message.reply("⚠️ <b>Invalid Format:</b> Use 10m, 1h, 1d or permanent.")
        return

    try:
        restrict_kwargs = {
            "chat_id": message.chat.id,
            "user_id": user_id,
            "permissions": permissions_mute,
        }
        if until_date != "permanent":
            restrict_kwargs["until_date"] = until_date

        await bot.restrict_chat_member(**restrict_kwargs)

        duration_text = "permanently" if until_date == "permanent" else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
        await message.reply(
            f"🚫 <b>Action:</b> User <b>{message.reply_to_message.from_user.first_name}</b> muted <b>{duration_text}</b>."
        )
    except Exception:
        await message.reply("🚨 <b>System Error:</b> Failed to restrict user.")


@user_group_router.message(Command("unmute"))
async def unmute_cmd(message: types.Message, bot: Bot):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("creator", "administrator"):
        return

    if not message.reply_to_message:
        await message.reply("❌ <b>Error:</b> Reply to the user you wish to unmute.")
        return

    try:
        user_id = message.reply_to_message.from_user.id
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=permissions_unmute,
        )
        await message.reply(
            f"✅ <b>Restored:</b> User <b>{message.reply_to_message.from_user.first_name}</b> unmuted."
        )
    except Exception as e:
        print(f"Error in unmute: {e}")
        await message.reply("🚨 <b>System Error:</b> Failed to lift restriction.")


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
        await message.answer(
            "⚠️ <b>Admin Notice:</b> Please maintain professional language."
        )
        return

    if warnings < 3:
        await message.answer(
            f"⚠️ <b>Warning {warnings}/3:</b> <b>{first_name}</b>, please refrain from using prohibited language in this chat.",
        )
        await message.delete()
        return

    users[user_id] = 0

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        permissions=permissions_mute,
        until_date=datetime.now() + timedelta(minutes=60),
    )

    await message.answer(
        text=f"🚫 <b>Access Restricted:</b> User <b>{first_name}</b> has reached the limit of <b>3/3 warnings</b>.\n<i>A 1-hour restriction has been applied.</i>",
    )
    await message.delete()


@user_group_router.my_chat_member()
async def on_bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member"):
        await event.answer(
            "🛡 <b>Profanity Filter Bot</b>\n\n"
            "I will automatically monitor this chat for prohibited language. "
            "Users receive warnings, and after <b>3/3</b> warnings, they are restricted for 1 hour.\n\n"
            "<b>Setup:</b>\n"
            "To function properly, I need administrator rights:\n"
            "1. Open Group Settings > <b>Administrators</b>\n"
            "2. Add me as an admin\n"
            "3. Enable <b>Delete Messages</b> and <b>Ban Users</b> permissions",
        )
