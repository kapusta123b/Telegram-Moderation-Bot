from string import punctuation

from datetime import datetime, timedelta

from asyncio import sleep

from aiogram import Bot, types, Router, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.filters.command import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config.strings as s
from database.requests import (
    add_ban,
    add_mute,
    add_warn,
    create_user,
    get_ban_list,
    get_mute_list,
    set_log_chat,
    get_log_chat,
)

from sqlalchemy.ext.asyncio import AsyncSession

from filters.group_filters import IsAdmin, CanBeRestricted
from filters.chat_filters import ChatTypeFilter

from config.config import (
    BAD_WORDS_FILE,
    permissions_mute,
    permissions_unmute,
    DEFAULT_MUTE_TIME,
)

from loguru import logger

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    BAD_WORDS = {line.strip().lower() for line in f if line.strip()}


def normalize(text: str) -> str:
    """
    Removes punctuation and converts text to lowercase for uniform comparison.
    """
    return text.translate(str.maketrans("", "", punctuation)).lower()


def contains_bad_word(text: str) -> bool:
    """
    Checks if the provided text contains any prohibited words from the blacklist.
    Supports both exact matches and substring detection.
    """
    normalized = normalize(text)
    words = normalized.split()

    if BAD_WORDS.intersection(words):
        return True

    for bad_word in BAD_WORDS:
        if bad_word in normalized:
            return True
    return False


def get_mute_duration(mutes_count: int) -> timedelta:
    """
    Calculates the duration of a mute based on the user's violation history.
    """
    
    if mutes_count <= 5:
        return DEFAULT_MUTE_TIME.get(mutes_count, timedelta(hours=1))

    base_time = timedelta(days=3).total_seconds()
    extra_mutes = mutes_count - 5
    multiplier = 1.5**extra_mutes
    return timedelta(seconds=base_time * multiplier)


def parse_time(time_str: str) -> datetime | str | None:
    """
    Parses a time string (for example, '1m') and returns a datetime object or "permanent".
    Uses a dictionary to map suffixes (m, h, d, w) to timedelta arguments.
    """
    if time_str == "permanent":
        return "permanent"

    unit = time_str[
        -1
    ]  # Extract the last character as the time unit (e.g., 'm' from '10m')
    units = {
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
    }  # Dictionary mapping suffixes to timedelta keywords

    if unit not in units:  # Return None if the unit is not supported
        return None

    try:
        value = int(
            time_str[:-1]
        )  # Extract the numeric value (everything except the last character) and convert to int
        # Return a future datetime based on the calculated interval
        return datetime.now() + timedelta(**{units[unit]: value})

    except ValueError:
        logger.warning(f"Failed to parse time string: {time_str}")

        return None


async def send_log(
    bot: Bot,
    session: AsyncSession,
    chat: types.Chat,
    user: types.User,
    action: str,
    duration: str = None,
    reason: str = None,
    message: types.Message = None,
):
    """
    Sends a log entry to the admin log channel if configured
    """
    log_chat_id = await get_log_chat(session)
    if not log_chat_id:
        return

    duration_text = (
        s.DURATION_TEXT.format(duration=duration)
        if duration else ""
    )

    reason_text = (
        s.REASON_LOG_TEXT.format(reason=reason)
        if reason else ""
    )

    log_text = s.MODERATION_LOG.format(
        first_name=user.first_name,
        user_id=user.id,
        action=action,
        duration_block=duration_text,
        reason_block=reason_text,
        chat_title=chat.title,
    )

    try:
        if message:
            await bot.forward_message(
                chat_id=log_chat_id, from_chat_id=chat.id, message_id=message.message_id
            )
        await bot.send_message(chat_id=log_chat_id, text=log_text)
        logger.debug(f"Log sent to chat {log_chat_id} for user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send log to chat {log_chat_id}: {e}")


async def handle_punishment(
    message: types.Message,
    bot: Bot,
    user: types.User,
    mutes: int,
    session: AsyncSession,
):
    """
    This function gives a mute for a time that depends on the number of user's mutes
    """

    duration = get_mute_duration(mutes)
    until_date = datetime.now() + duration

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user.id,
        permissions=permissions_mute,
        until_date=until_date,
    )

    logger.info(f"Auto-punishment applied to user {user.id} in chat {message.chat.id} (Mute #{mutes})")

    hours = int(duration.total_seconds() // 3600)
    days = hours // 24
    duration_str = f"{days} days" if days > 0 else f"{hours} hours"

    await send_log(
        bot=bot,
        session=session,
        chat=message.chat,
        user=user,
        action="Auto-Mute (3/3 Warnings)",
        duration=duration_str,
        message=message,
    )

    await message.reply(
        text=s.ACCESS_RESTRICTED.format(
        first_name=user.first_name,
        warnings=3,
        duration=duration_str,
        mute_count=mutes
        )
    )


@user_group_router.message(Command("warn"), IsAdmin())
async def warn_cmd(message: types.Message, bot: Bot, session: AsyncSession):
    """
    Manual warning command for administrators to discipline users.
    """
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        # Increment warnings and get current stats
        current_warns, mutes = await add_warn(session, target_user.id)

        if current_warns < 3:
            logger.info(f"Admin {message.from_user.id} issued warning {current_warns}/3 to user {target_user.id} in chat {message.chat.id}")
            await send_log(
                bot=bot,
                session=session,
                chat=message.chat,
                user=target_user,
                action=f"Warning ({current_warns}/3)",
                message=message.reply_to_message,
            )

            await message.reply(
                text=s.ACTION_WARN_TO.format(
                    first_name=target_user.first_name,
                    current_warns=current_warns
                )
            )

        else:
            await handle_punishment(
                message.reply_to_message, bot, target_user, mutes, session
            )

    else:
        await message.reply(s.NOTICE_REPLY)


@user_group_router.message(Command("mute"), IsAdmin(), CanBeRestricted())
async def mute_cmd(
    message: types.Message, command: CommandObject, bot: Bot, session: AsyncSession
):
    """
    The handler temporarily mute the user, either by replying to a message or by ID
    """

    if not message.reply_to_message and not command.args:
        await message.reply(
            s.NOT_REPLY_TO_MESSAGE
        )
        return

    user_id = (
        # Get user ID from the replied-to message if the command is a reply
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else None
    )

    # takes the first argument if command.args
    time_or_id_arg = command.args.split()[0].lower() if command.args else "permanent"

    # if user_id is None and if time_or_id_arg consists of numbers, then it means that there is a user ID there
    if (user_id is None and time_or_id_arg.isdigit()):
        # convert the ID string to an int
        user_id = int(time_or_id_arg)

        # permanent if nothing was passed in the arguments except the ID, otherwise we take the ban time
        time_or_id_arg = (
            "permanent"
            if len(command.args.split()) < 2
            else command.args.split()[1].lower()
        )

    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
    until_date = parse_time(time_or_id_arg)
    set_arg = True if "set" in command.args.split() else None

    if until_date is None:
        await message.reply(
            s.INVALID_FORMAT
            )
        
        return

    try:
        restrict_kwargs = {
            "chat_id": message.chat.id,
            "user_id": user_id,
            "permissions": permissions_mute,
        }

        if (
            until_date != "permanent"
        ):  # If not permanent, specify the expiration date for the restriction
            restrict_kwargs["until_date"] = until_date

        if (
            target.status != "restricted"
            or getattr(target, "can_send_messages", True)
            or set_arg
        ):
            await bot.restrict_chat_member(
                **restrict_kwargs
            )  # Unpack arguments and call the restriction method

            reason = (
                " ".join(
                    [
                        word
                        for word in command.args.split(" ")[1:]
                        if word.lower() != "set"
                    ]
                )
                if command.args and len(command.args.split(" ")) >= 2
                else None
            )

            duration_text = (
                "permanently"
                if until_date
                == "permanent"  # Check if parse_time returned the "permanent" flag
                else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
            )

            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )

            status_text = "mute extended" if set_arg else "muted"

            logger.info(f"Admin {message.from_user.id} {status_text} user {user_id} in chat {message.chat.id} {duration_text}")

            await send_log(
                bot=bot,
                session=session,
                chat=message.chat,
                user=(
                    message.reply_to_message.from_user
                    if message.reply_to_message
                    else target.user
                ),
                action="Mute" if not set_arg else "Mute Extended",
                duration=duration_text,
                reason=reason,
                message=(
                    message.reply_to_message if message.reply_to_message else message
                ),
            )

            await add_mute(
                session=session,
                user_id=user_id,
                name=name,
                time=datetime.now(),
                duration=duration_text,
                reason=reason,
                status=status_text,
            )  

            reason_block = (
                s.REASON_BLOCK.format(reason=reason)
                if reason else ""
            )

            await message.reply(
                text=s.ACTION_USER.format(
                    name=name,
                    status_text=status_text,
                    duration_text=duration_text,
                    reason=reason_block
                )
            )

        else:
            await message.reply(
                text=s.ALREADY_MUTED
            )

    except Exception:
        await message.reply(s.SYSTEM_ERROR_MUTE)
        logger.exception('Failed to mute user')


@user_group_router.message(Command("unmute"), IsAdmin(), CanBeRestricted())
async def unmute_cmd(message: types.Message, bot: Bot, session: AsyncSession):
    user_id = message.reply_to_message.from_user.id
    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)

    try:
        if target.status == "restricted":
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=permissions_unmute,
            )

            logger.info(f"Admin {message.from_user.id} unmuted user {user_id} in chat {message.chat.id}")

            await send_log(
                bot=bot,
                session=session,
                chat=message.chat,
                user=message.reply_to_message.from_user,
                action="Unmute",
                message=message,
            )

            await message.reply(
                text=s.RESTORED_USER_UNMUTE.format(
                    first_name=message.reply_to_message.from_user.first_name
                )
            )

    except Exception:
        await message.reply(s.SYSTEM_ERROR_UNMUTE)
        logger.exception(f"Failed to unmute user {user_id} in chat {message.chat.id}")


@user_group_router.message(Command("ban"), IsAdmin(), CanBeRestricted())
async def ban_cmd(
    message: types.Message, command: CommandObject, bot: Bot, session: AsyncSession
):
    """
    The handler temporarily bans the user, either by replying to a message or by ID
    """

    if not message.reply_to_message and not command.args:
        await message.reply(s.NOT_REPLY_TO_MESSAGE)
        return

    user_id = (
        # get user ID from the replied-to message if the command is a reply
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else None
    )

    # takes the first argument if command.args
    time_or_id_arg = command.args.split()[0].lower() if command.args else "permanent"
    
    # if user_id is None and if time_or_id_arg consists of numbers, then it means that there is a user ID there
    if (user_id is None and time_or_id_arg.isdigit()):  
        # convert the ID string to an int
        user_id = int(time_or_id_arg)
        
        # permanent if nothing was passed in the arguments except the ID, otherwise we take the ban time
        time_or_id_arg = (
            "permanent"
            if len(command.args.split()) < 2
            else command.args.split()[1].lower()
        )

    target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
    until_date = parse_time(time_or_id_arg) # permanent or time (example: 10m)

    set_arg = True if "set" in command.args.split() else None

    try:
        if target.status != "kicked" or set_arg:
            await bot.ban_chat_member(
                chat_id=message.chat.id, user_id=user_id, until_date=until_date
            )

            duration_text = (
                "permanently"
                if until_date
                in (
                    "permanent",
                    None,
                )  # Default to permanent if no argument is provided or "permanent" is explicitly used
                else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"  # Format the expiration date if an interval was provided
            )

            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )

            reason = (
                " ".join(
                    [
                        word
                        for word in command.args.split(" ")[1:]
                        if word.lower() != "set"
                    ]
                )
                if command.args and len(command.args.split(" ")) >= 2
                else None
            )

            status_text = "ban extended" if set_arg else "banned"

            logger.info(f"Admin {message.from_user.id} {status_text} user {user_id} in chat {message.chat.id} {duration_text}")

            await send_log(
                bot=bot,
                session=session,
                chat=message.chat,
                user=(
                    message.reply_to_message.from_user
                    if message.reply_to_message
                    else target.user
                ),
                action="Ban" if not set_arg else "Ban Extended",
                duration=duration_text,
                reason=reason,
                message=(
                    message.reply_to_message if message.reply_to_message else message
                ),
            )

            reason_block = (
                s.REASON_BLOCK.format(reason=reason)
                if reason else ""
            )

            await add_ban(
                session=session,
                user_id=user_id,
                time=datetime.now(),
                name=name,
                duration=duration_text,
                reason=reason,
                status=status_text,
            )

            await message.reply(
                text=s.ACTION_USER.format(
                    name=name,
                    status_text=status_text,
                    duration_text=duration_text,
                    reason=reason_block
                )
            )
        else:
            await message.reply(
                s.ALREADY_BANNED
            )

    except Exception:
        await message.reply(s.SYSTEM_ERROR_BAN)
        logger.exception(f"Failed to ban user {user_id} in chat {message.chat.id}")


@user_group_router.message(Command("unban"), IsAdmin(), CanBeRestricted())
async def unban_cmd(
    message: types.Message, command: CommandObject, bot: Bot, session: AsyncSession
):
    """
    The handler unbans the user by replying to a message or by ID
    """

    if not command.args and not message.reply_to_message:
        await message.reply(s.NOT_REPLY_TO_MESSAGE)
        return

    try:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id

        else: # get the ID from the message if there is no reply_to_message
            user_id = int(command.args.split()[0])

        target = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)

        if target.status == "kicked": # only unban if he was kicked out of the group.
            await bot.unban_chat_member(
                chat_id=message.chat.id, user_id=user_id, only_if_banned=True
            )

            logger.info(f"Admin {message.from_user.id} unbanned user {user_id} in chat {message.chat.id}")

            name = (
                message.reply_to_message.from_user.first_name
                if message.reply_to_message
                else f"ID: {user_id}"
            )

            await send_log(
                bot=bot,
                session=session,
                chat=message.chat,
                user=(
                    message.reply_to_message.from_user
                    if message.reply_to_message
                    else target.user
                ),
                action="Unban",
                message=message,
            )

            await message.reply(text=s.RESTORED_USER_BAN.format(
                name=name  
                )
            )


        else:
            await message.reply(
                s.USER_IS_NOT_BANNED
            )

    except ValueError:
        await message.reply(s.VALUE_UNBAN_ERROR)
        logger.warning(f"Invalid User ID provided for unban in chat {message.chat.id}")

    except Exception:
        await message.reply(s.SYSTEM_ERROR_UNBAN)
        logger.exception(f"Failed to unban user {user_id} in chat {message.chat.id}")


@user_group_router.message(Command("report"))
async def report_cmd(
    message: types.Message, command: CommandObject, bot: Bot, session: AsyncSession
):
    """
    This handler sends a log as a report to the admin channel.
    """

    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        
        reporter = message.from_user

        reason = command.args if command.args else "No reason provided"

        await send_log(
            bot=bot,
            session=session,
            chat=message.chat,
            user=target_user,
            action=f"Reported by {reporter.first_name}",
            message=message.reply_to_message,
            reason=reason,
        )

        await message.reply(
            s.REPORT_SENT
        )

    else:
        await message.reply(s.REPORT_NO_REPLY)


@user_group_router.message(Command("ban_list"), IsAdmin())
async def ban_list_cmd(message: types.Message, command: CommandObject, session: AsyncSession):
    """
    The handler sends a list of baned users
    """

    # returns a list of users who have ever been baned
    bans = await get_ban_list(session)

    if not bans:
        await message.reply(s.BAN_NO_RECORDS)
        return
    
    # if arguments are passed, it takes the first argument (the number of users to be displayed), otherwise 0
    number_of_users = int(command.args.split()[0]) if command.args else 0

    history_scope = (
        f"{number_of_users} <b>Users</b>"
        if number_of_users
        else "Full history"
    )

    text = s.BAN_HISTORY_HEADER.format(history_scope=history_scope)

    for ban in bans[-number_of_users:]: # the number of users is taken depending on the number in number_of_users
        date_str = ban.time.strftime("%Y-%m-%d %H:%M") # formatting into a convenient form

        reason_text = ban.reason if ban.reason else "None"

        text += s.LIST_RECORD.format(
            name=ban.name,
            user_id=ban.user_id,
            date=date_str,
            duration=ban.duration,
            reason=reason_text,
        )

    await message.reply(text)


@user_group_router.message(Command("mute_list"), IsAdmin())
async def mute_list_cmd(message: types.Message, session: AsyncSession, command: CommandObject):
    """
    The handler sends a list of muted users
    """
    
    # returns a list of users who have ever been muted
    mutes = await get_mute_list(session)

    if not mutes:
        await message.reply(s.MUTE_NO_RECORDS)
        return

    # if arguments are passed, it takes the first argument (the number of users to be displayed), otherwise 0
    number_of_users = int(command.args.split()[0]) if command.args else 0
    
    history_scope = (
        f"{number_of_users} <b>Users</b>"
        if number_of_users
        else "Full history"
    )

    text = s.MUTE_HISTORY_HEADER.format(history_scope=history_scope)

    for mute in mutes[-number_of_users:]: # the number of users is taken depending on the number in number_of_users
        date_str = mute.time.strftime("%Y-%m-%d %H:%M") # formatting into a convenient form
        
        reason_text = mute.reason if mute.reason else "None"

        text += s.LIST_RECORD.format(
            name=mute.name,
            user_id=mute.user_id,
            date=date_str,
            duration=mute.duration,
            reason=reason_text,
        )

    await message.reply(text)


@user_group_router.message(F.new_chat_members | F.left_chat_member)
async def delete_system_message(message: types.Message, session: AsyncSession):
    """
    This handler deletes the system message when someone leaves or enters the group, saving it to the database.
    """

    if message.new_chat_members:
        for member in message.new_chat_members:
            if not member.is_bot:
                await create_user(session, member.id)

    elif message.left_chat_member:
        if not message.left_chat_member.is_bot:
            await create_user(session, message.left_chat_member.id)

    try:
        await message.delete()

    except Exception:
        logger.debug(f"Could not delete system message in chat {message.chat.id}")


@user_group_router.message(Command("admin_chat"), IsAdmin())
async def set_admin_chat(message: types.Message, session: AsyncSession):
    """
    This handler writes the chat.id to the database, which will be used to send admin logs.
    """

    log_chat_id = message.chat.id

    try:
        await set_log_chat(session, log_chat_id)

        await message.reply(
            s.SUCCESS_SET_CHAT
        )

    except ValueError:
        await message.reply(
            s.ALREADY_CONFIGURED
        )
        logger.info(f"Admin chat already configured for chat {message.chat.id}")


@user_group_router.edited_message
@user_group_router.message()
async def cleaner(message: types.Message, bot: Bot, session: AsyncSession):
    """
    Main message filter that scans for profanity and manages warnings/mutes.
    """
    if message.from_user.is_bot:
        return

    content = message.text or message.caption
    if not content:
        return

    if not contains_bad_word(content):
        return

    user = message.from_user
    member = await bot.get_chat_member(message.chat.id, user.id)

    if member.status in ("creator", "administrator"):
        await message.reply(
            s.ADMIN_NOTICE
        )

        return

    current_warns, mutes = await add_warn(session, user.id)

    if current_warns < 3:
        logger.info(f"Message from {user.id} in chat {message.chat.id} deleted (bad word). Warnings: {current_warns}/3")
        await message.reply(
            text=s.SENT_AUTO_WARN.format(
                current_warns=current_warns,
                first_name=user.first_name
            ),
        )

        await message.delete()

        return

    else:
        await handle_punishment(
            message=message, bot=bot, user=user, mutes=mutes, session=session
        )


@user_group_router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def captcha(event: types.ChatMemberUpdated, session: AsyncSession):
    """
    This handler automatically mutes the user when they join until they press the button.
    """

    user_id = event.new_chat_member.user.id

    await event.bot.restrict_chat_member(
        chat_id=event.chat.id, user_id=user_id, permissions=permissions_mute
    )

    builder = InlineKeyboardBuilder().add(
        types.InlineKeyboardButton(
            text="✅ I'm not a robot!", callback_data=f"not_bot:{user_id}"
        )
    )

    captcha_msg = await event.bot.send_message(
        chat_id=event.chat.id,
        text=s.VERIFICATION_TEXT.format(first_name=event.new_chat_member.user.first_name),
        reply_markup=builder.as_markup(),
    )

    await sleep(300)

    current_member = await event.bot.get_chat_member(
        chat_id=event.chat.id, user_id=user_id
    )

    if (
        current_member.status == "restricted" and not current_member.can_send_messages
    ) or current_member.status in ("left", "kicked"):
        logger.info(f"User {user_id} failed captcha in chat {event.chat.id}")
        await send_log(
            bot=event.bot,
            session=session,
            chat=event.chat,
            user=event.new_chat_member.user,
            action="Banned (Captcha Failed)",
            duration="24 hours",
        )

        await event.bot.send_message(
            chat_id=event.chat.id,
            text=s.VERIFICATION_FAILED.format(first_name=event.new_chat_member.user.first_name),
        )

        await event.bot.ban_chat_member(
            chat_id=event.chat.id,
            user_id=user_id,
            until_date=datetime.now() + timedelta(days=1),
        )

        try:
            await captcha_msg.delete()

        except Exception:
            logger.debug(f"Could not delete captcha message in chat {event.chat.id}")


@user_group_router.callback_query(F.data.startswith("not_bot:"))
async def captcha_unmute(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split(":")[1])

    if callback.from_user.id == target_user_id:
        logger.info(f"User {target_user_id} successfully passed captcha in chat {callback.message.chat.id}")
        await callback.bot.restrict_chat_member(
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            permissions=permissions_unmute,
        )

        await callback.answer(
            text=s.VERIFICATION_SUCCES, show_alert=True
        )

        await callback.message.delete()

    else:
        await callback.answer(s.VERIFICATION_NOT_FOR_YOU, show_alert=True)
        return


@user_group_router.my_chat_member()
async def on_bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator"):
        logger.info(f"Bot added to chat {event.chat.id} ({event.chat.title})")
        await event.bot.send_message(
            chat_id=event.chat.id,
            text=s.WELCOME_TEXT_GROUP
        )