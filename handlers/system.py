from aiogram import types, Router, F
from aiogram.filters.command import CommandObject, Command

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from config.config import MAX_WARNS

from database.requests import create_user, set_log_chat, unset_log_chat

from filters.group_filters import IsAdmin
from filters.chat_filters import ChatTypeFilter


from loguru import logger

system_router = Router()
system_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@system_router.message(F.new_chat_members | F.left_chat_member)
async def delete_system_message(message: types.Message, session: AsyncSession):
    """
    This handler deletes the system message when someone leaves or enters the group, saving it to the database.
    """

    if message.new_chat_members:
        for member in message.new_chat_members:
            if not member.is_bot:
                await create_user(session, member.id, message.chat.id)

    elif message.left_chat_member:
        if not message.left_chat_member.is_bot:
            await create_user(session, message.left_chat_member.id, message.chat.id)

    await session.commit()

    try:
        await message.delete()

    except Exception:
        logger.debug(f"Could not delete system message in chat {message.chat.id}")


@system_router.message(Command("set_admin_chat", "unset_admin_chat"), IsAdmin())
async def set_admin_chat(
    message: types.Message, session: AsyncSession, command: CommandObject
):
    """
    This handler manages the admin log channel configuration.
    """

    action = command.command

    try:
        if action == "set_admin_chat":
            await set_log_chat(session, message.chat.id, message.chat.id)
            await message.reply(s.SUCCESS_SET_CHAT)

        else:
            await unset_log_chat(session, message.chat.id)
            await message.reply(s.SUCCESS_UNSET_CHAT)

    except ValueError as e:
        if action == "set_admin_chat":
            await message.reply(s.ALREADY_CONFIGURED)

        else:
            await message.reply(s.NOT_CONFIGURED)

        logger.info(f"Admin chat {action} skipped: {e}")

    except Exception:
        logger.exception(f"Failed to {action} for chat {message.chat.id}")
        await message.reply(s.SYSTEM_ERROR)

    await session.commit()


@system_router.my_chat_member()
async def on_bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator"):
        logger.info(f"Bot added to chat {event.chat.id} ({event.chat.title})")
        await event.bot.send_message(
            chat_id=event.chat.id, text=s.WELCOME_TEXT_GROUP.format(max_warns=MAX_WARNS)
        )