from pathlib import Path

from string import punctuation

from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

from filters.group_filters import IsAdmin, CanBeRestricted
from filters.chat_filters import ChatTypeFilter

from datetime import datetime, timedelta


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
    """
    Parses a time string (for example, '1m') and returns a datetime object or "permanent".
    Uses a dictionary to map suffixes (m, h, d, w) to timedelta arguments.
    """
    if time_str == "permanent":
        return "permanent"

    unit = time_str[-1] # Extract the last character as the time unit (e.g., 'm' from '10m')
    units = {"m": "minutes", "h": "hours", "d": "days", "w": "weeks"} # Dictionary mapping suffixes to timedelta keywords

    if unit not in units: # Return None if the unit is not supported
        return None

    try:
        # Extract the numeric value (everything except the last character) and convert to int
        value = int(time_str[:-1])

        # Return a future datetime based on the calculated interval
        return datetime.now() + timedelta(**{units[unit]: value}) 
        

    except ValueError:
        return None


@user_group_router.message(Command("mute"), IsAdmin(), CanBeRestricted())
async def mute_cmd(message: types.Message, command: CommandObject, bot: Bot):
    if not message.reply_to_message and not command.args:
        await message.reply(
            "❌ <b>Error:</b> Provide duration or reply to a message (e.g., <code>/mute 10m</code>)."
        )
        return
    
    user_id = (
        # Get user ID from the replied-to message if the command is a reply
        message.reply_to_message.from_user.id if message.reply_to_message else None 
    )
    time_arg = command.args.split()[0].lower() if command.args else "permanent"

    if user_id is None and time_arg.isdigit(): # If no reply, attempt to parse the first argument as a User ID
        user_id = int(time_arg)
        time_arg = (
            "permanent"
            if len(command.args.split()) < 2
            else command.args.split()[1].lower()
        )

    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
    until_date = parse_time(time_arg)
    set_arg = (True if 'set' in command.args.split() else None)

    if until_date is None:
        await message.reply("⚠️ <b>Invalid Format:</b> Use 10m, 1h, 1d or permanent.")
        return

    try:
        restrict_kwargs = {
            "chat_id": message.chat.id,
            "user_id": user_id,
            "permissions": permissions_mute,
        }
        if until_date != "permanent": # If not permanent, specify the expiration date for the restriction
            restrict_kwargs["until_date"] = until_date 

        if target.status != 'restricted' or set_arg:
            await bot.restrict_chat_member(**restrict_kwargs) # Unpack arguments and call the restriction method

            description = (
                '\n<b>Description:</b> ' + ' '.join([word for word in command.args.split(' ')[1:] if word.lower() != 'set'])
                if len(command.args.split(" ")) >= 2
                else None
            )

            duration_text = (
                "permanently"
                if until_date == "permanent" # Check if parse_time returned the "permanent" flag
                else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
            )

            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )

            status_text = ",mute has been extended" if set_arg else " muted"
            await message.reply(
                f"🚫 <b>Action:</b> User <b>{name}</b>{status_text} <b>{duration_text}</b>. {description if description else ''}"
            )
        else:
            await message.reply(
                "⚠️ <b>Notice:</b> This user is already muted. Use the <code>set</code> argument to update the duration (e.g., <code>/mute 10m set</code>)."
            )
    except Exception:
        await message.reply("🚨 <b>System Error:</b> Failed to restrict user.")


@user_group_router.message(Command("unmute"), IsAdmin(), CanBeRestricted())
async def unmute_cmd(message: types.Message, bot: Bot):
    user_id = message.reply_to_message.from_user.id
    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
    try:
        if target.status == 'restricted':
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=permissions_unmute,
            )
            await message.reply(
                f"✅ <b>Restored:</b> User <b>{message.reply_to_message.from_user.first_name}</b> unmuted."
            )

    except Exception:
        await message.reply("🚨 <b>System Error:</b> Failed to lift restriction.")


@user_group_router.message(Command("ban"), IsAdmin(), CanBeRestricted())
async def ban_cmd(message: types.Message, command: CommandObject, bot: Bot):
    if not message.reply_to_message and not command.args:
        await message.reply("❌ <b>Error:</b> Provide duration or reply to a message.")
        return
    

    user_id = (
        # get user ID from the replied-to message if the command is a reply
        message.reply_to_message.from_user.id if message.reply_to_message else None 
    )
    time_or_id_arg = command.args.split()[0].lower() if command.args else "permanent"

    if user_id is None and time_or_id_arg.isdigit(): # if no reply, attempt to parse the first argument as a User ID
        user_id = int(time_or_id_arg)
        time_or_id_arg = (
            "permanent"
            if len(command.args.split()) < 2
            else command.args.split()[1].lower()
        )

    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
    until_date = parse_time(time_or_id_arg)
    set_arg = (True if 'set' in command.args.split() else None)

    try:
        if target.status != 'kicked' or set_arg:
            await bot.ban_chat_member(
                chat_id=message.chat.id, user_id=user_id, until_date=until_date
            )
            duration_text = (
                "permanently" 
                if until_date in ("permanent", None) # Default to permanent if no argument is provided or "permanent" is explicitly used
                else f"until {until_date.strftime('%Y-%m-%d %H:%M')}" # Format the expiration date if an interval was provided
            )
            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )
            description = (
                '\n<b>Description:</b> ' + ' '.join([word for word in command.args.split(' ')[1:] if word.lower() != 'set'])
                if len(command.args.split(" ")) >= 2
                else None
            )
            
            status_text = ",ban has been extended" if set_arg else " banned"
            await message.reply(
                f"🚫 <b>Action:</b> User <b>{name}</b>{status_text} <b>{duration_text}</b>. {description if description else ''}"
            )
        else:
            await message.reply(
                "⚠️ <b>Notice:</b> This user is already banned. Use the <code>set</code> argument to update the duration (e.g., <code>/ban 10m set</code>)."
            )

    except Exception:
        await message.reply("🚨 <b>System Error:</b> Failed to ban user.")

@user_group_router.message(Command("unban"), IsAdmin(), CanBeRestricted())
async def unban_cmd(message: types.Message, command: CommandObject, bot: Bot):
    if not command.args and not message.reply_to_message:
        await message.reply("❌ <b>Error:</b> Provide User ID or reply to a message.")
        return

    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = int(command.args.split()[0])

        target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)

        if target.status == "kicked":
            await bot.unban_chat_member(
                chat_id=message.chat.id, user_id=user_id, only_if_banned=True
            )

            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )
            await message.reply(f"✅ <b>Restored:</b> User <b>{name}</b> unbanned.")
        else:
            await message.reply("ℹ️ <b>Info:</b> User is not banned or is already a member.")

    except ValueError:
        await message.reply("⚠️ <b>Invalid Format:</b> Use numeric User ID.")
    except Exception:
        await message.reply("🚨 <b>System Error:</b> Failed to unban user.")


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
