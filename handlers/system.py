from aiogram import types, Router, F
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from database.requests import create_user, set_log_chat
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
                await create_user(session, member.id)

    elif message.left_chat_member:
        if not message.left_chat_member.is_bot:
            await create_user(session, message.left_chat_member.id)

    try:
        await message.delete()

    except Exception:
        logger.debug(f"Could not delete system message in chat {message.chat.id}")


@system_router.message(Command("admin_chat"), IsAdmin())
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


@system_router.my_chat_member()
async def on_bot_added_to_group(event: types.ChatMemberUpdated):
    if event.new_chat_member.status in ("member", "administrator"):
        logger.info(f"Bot added to chat {event.chat.id} ({event.chat.title})")
        await event.bot.send_message(
            chat_id=event.chat.id,
            text=s.WELCOME_TEXT_GROUP
        )
