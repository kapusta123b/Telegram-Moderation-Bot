from html import escape
from aiogram import types, Bot

from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import get_log_chat

import config.strings as s

from loguru import logger


async def send_log(
    bot: Bot,
    session: AsyncSession,
    chat: types.Chat | int,
    user: types.User,
    action: str,
    duration: str = None,
    reason: str = None,
    message: types.Message = None,
):
    """
    Sends a log entry to the admin log channel if configured
    """

    if isinstance(chat, int):
        chat_id = chat
        
    else:
        chat_id = chat.id

    log_chat_id = await get_log_chat(session, chat_id)
    if not log_chat_id:
        return

    if isinstance(chat, int):
        try:
            chat_obj = await bot.get_chat(chat)
            chat_title = chat_obj.title
            chat_id = chat

        except Exception:
            chat_title = f"ID: {chat}"
            chat_id = chat
            
    else:
        chat_title = chat.title
        chat_id = chat.id

    duration_text = (
        s.DURATION_TEXT.format(duration=escape(duration))
        if duration else ""
    )

    reason_text = (
        s.REASON_LOG_TEXT.format(reason=escape(reason))
        if reason else ""
    )

    log_text = s.MODERATION_LOG.format(
        first_name=escape(user.first_name),
        user_id=user.id,
        action=escape(action),
        duration_block=duration_text,
        reason_block=reason_text,
        chat_title=escape(chat_title),
    )

    try:
        if message:
            await bot.forward_message(
                chat_id=log_chat_id, from_chat_id=chat_id, message_id=message.message_id
            )
            
        await bot.send_message(chat_id=log_chat_id, text=log_text)
        logger.debug(f"Log sent to chat {log_chat_id} for user {user.id}")

    except Exception as e:
        logger.error(f"Failed to send log to chat {log_chat_id}: {e}")
