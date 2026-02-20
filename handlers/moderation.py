from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

from sqlalchemy.ext.asyncio import AsyncSession

from config.config import MAX_WARNS
import config.strings as s

from filters.group_filters import IsAdmin
from filters.chat_filters import ChatTypeFilter

from loguru import logger

from services.restriction_service import (
    RestrictionService,
    AlreadyRestrictedError,
    NotRestrictedError,
    AlreadyBannedError,
    ZeroCurrentWarns,
)

from utils.time import parse_time
from utils.text import contains_bad_word, contains_link

moderation_router = Router()
moderation_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@moderation_router.message(Command("warn", "unwarn"), IsAdmin())
async def warn_cmd(
    message: types.Message, bot: Bot, session: AsyncSession, command: CommandObject
):
    """
    Manual warning command for administrators to discipline users.
    """

    if not message.reply_to_message:
        await message.reply(s.NOTICE_REPLY)
        return

    action = command.command

    target_user = message.reply_to_message.from_user
    service = RestrictionService(bot, session)

    if action == "warn":
        result = await service.warn(
            chat_id=message.chat.id, user=target_user, message=message.reply_to_message
        )
    else:
        try:
            result = await service.unwarn(
                message.chat.id, target_user, message.reply_to_message
            )
        except ZeroCurrentWarns:
            await message.reply(text=s.ZERO_CURRENT_WARNS)
            return

    if result["status"] == "warned":
        await message.reply(
            text=s.ACTION_WARN_TO.format(
                first_name=target_user.first_name,
                current_warns=result["current_warns"],
                max_warns=MAX_WARNS,
            )
        )

    elif result["status"] == "auto_muted":
        # auto-muted after MAX_WARNS warns
        await message.reply(
            text=s.ACCESS_RESTRICTED.format(
                first_name=target_user.first_name,
                warnings=MAX_WARNS,
                max_warns=MAX_WARNS,
                duration=result["duration"],
                mute_count=result["mute_count"],
            )
        )

    elif result["status"] == "unwarned":
        await message.reply(
            text=s.ACTION_UNWARN_TO.format(
                first_name=target_user.first_name,
                current_warns=result["current_warns"],
                max_warns=MAX_WARNS,
            )
        )

    await session.commit()


@moderation_router.message(
    Command("mute", "ban", "unmute", "unban"),
    IsAdmin(),
)
async def restriction_cmd(
    message: types.Message,
    command: CommandObject,
    bot: Bot,
    session: AsyncSession,
):
    """
    Unified handler for restriction commands (mute, ban, unmute, unban).
    Supports both reply to message and explicit User ID.
    """

    if not message.reply_to_message and not command.args:
        await message.reply(s.NOT_REPLY_TO_MESSAGE)
        return

    action = command.command
    args = command.args.split() if command.args else []

    # identify target user
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user

    else:
        if not args or not args[0].isdigit():
            await message.reply(s.INVALID_FORMAT)
            return

        user_id = int(args[0])
        args = args[1:]

        try:
            member = await bot.get_chat_member(message.chat.id, user_id)
            target_user = member.user

        except Exception:
            # if we can't get user info, we can't proceed because service needs name
            await message.reply(s.SYSTEM_ERROR_MUTE)
            return

    # parse common arguments
    extend = "set" in [a.lower() for a in args]
    args = [a for a in args if a.lower() != "set"]

    until_date = None
    reason = None

    if action in ("mute", "ban"):
        time_arg = args[0] if args else "permanent"
        until_date = parse_time(time_arg)

        if until_date is None:
            await message.reply(s.INVALID_FORMAT)
            return

        if until_date == "permanent":
            until_date = None

        reason = " ".join(args[1:]) if len(args) > 1 else None

    service = RestrictionService(bot, session)

    try:
        if action == "mute":
            result = await service.mute(
                message.chat.id,
                target_user,
                until_date,
                reason,
                extend,
                message.reply_to_message,
            )

        elif action == "ban":
            result = await service.ban(
                message.chat.id,
                target_user,
                until_date,
                reason,
                extend,
                message.reply_to_message,
            )

        elif action == "unmute":
            result = await service.unmute(
                message.chat.id, target_user, message.reply_to_message
            )

        elif action == "unban":
            result = await service.unban(
                message.chat.id, target_user, message.reply_to_message
            )

    except AlreadyRestrictedError:
        await message.reply(s.ALREADY_MUTED)
        return

    except NotRestrictedError:
        await message.reply(s.SYSTEM_ERROR_UNMUTE)
        return

    except AlreadyBannedError:
        await message.reply(s.ALREADY_BANNED)
        return

    except PermissionError:
        await message.reply(s.ADMIN_NOTICE)
        return

    except Exception as e:
        logger.exception(f"Action {action} failed, {e}")
        await message.reply(s.SYSTEM_ERROR_MUTE)
        return

    # success response
    duration_text = (
        "permanently"
        if until_date is None
        else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
    )

    status_map = {
        "mute": "muted",
        "ban": "banned",
        "unmute": "unmuted",
        "unban": "unbanned",
    }

    await message.reply(
        s.ACTION_USER.format(
            name=target_user.full_name,
            status_text=status_map[action],
            duration_text=duration_text if action in ("mute", "ban") else "",
            reason_block=s.REASON_BLOCK.format(reason=reason) if reason else "",
        )
    )

    await session.commit()


@moderation_router.edited_message
@moderation_router.message()
async def cleaner(message: types.Message, bot: Bot, session: AsyncSession):
    """
    Main message filter that scans for profanity and manages warnings/mutes.
    """

    if message.from_user.is_bot:
        return

    content = message.text or message.caption

    if not content:
        return

    if contains_link(content):
        await message.reply(s.ADS_MESSAGE)

        try:
            await message.delete()

        except Exception:
            logger.debug(
                f"Could not delete message with profanity in chat {message.chat.id}"
            )

    if not contains_bad_word(content):
        return

    user = message.from_user
    member = await bot.get_chat_member(message.chat.id, user.id)

    if member.status in ("creator", "administrator"):
        await message.reply(s.ADMIN_NOTICE)

        return

    service = RestrictionService(bot, session)
    result = await service.warn(
        chat_id=message.chat.id, user=user, message=message, reason="Profanity filter"
    )

    if result["status"] == "warned":
        logger.info(
            f"Message from {user.id} in chat {message.chat.id} deleted (bad word). Warnings: {result['current_warns']}/{MAX_WARNS}"
        )
        await message.reply(
            text=s.SENT_AUTO_WARN.format(
                first_name=user.first_name,
                current_warns=result["current_warns"],
                max_warns=MAX_WARNS,
            )
        )
    else:
        # auto-muted after MAX_WARNS warns
        await message.reply(
            text=s.ACCESS_RESTRICTED.format(
                first_name=user.first_name,
                warnings=MAX_WARNS,
                max_warns=MAX_WARNS,
                duration=result["duration"],
                mute_count=result["mute_count"],
            )
        )

    await session.commit()

    try:
        await message.delete()

    except Exception:
        logger.debug(
            f"Could not delete message with profanity in chat {message.chat.id}"
        )
