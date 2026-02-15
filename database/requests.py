from datetime import datetime

from config.config import MAX_WARNS
from database.models import BanHistory, MuteHistory, User, ChatConfig

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from loguru import logger


async def create_user(session: AsyncSession, user_id, chat_id):
    """
    Ensures a user exists in the database. Creates a new record if not found.
    """
    user = await session.get(User, (user_id, chat_id))

    if not user:
        new_user = User(id=user_id, chat_id=chat_id)
        session.add(new_user)
        logger.info(f"New user {user_id} in chat {chat_id} created in database")
    


async def add_warn(session: AsyncSession, user_id, chat_id):
    """
    Increments the warning count for a user. Triggers mute status if limit reached.
    """
    user = await session.get(User, (user_id, chat_id))
    
    if not user:
        user = User(id=user_id, chat_id=chat_id)
        session.add(user)

    user.count_warns = (user.count_warns or 0) + 1

    current_warns = user.count_warns

    if user.count_warns >= MAX_WARNS:
        user.count_warns = 0
        user.count_mutes = (user.count_mutes or 0) + 1
        user.is_muted = True

    mutes = user.count_mutes or 0

    return current_warns, mutes


async def add_mute(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    time: datetime,
    name: str,
    status: str,
    duration: str,
    reason: str = None,
):
    """
    Logs a new mute action to the database history.
    """
    user = await session.get(User, (user_id, chat_id))
    if not user:
        user = User(id=user_id, chat_id=chat_id)
        session.add(user)

    user.count_mutes = (user.count_mutes or 0) + 1
    user.is_muted = True

    new_record = MuteHistory(
        user_id=user_id,
        chat_id=chat_id,
        time=time,
        name=name,
        status=status,
        duration=duration,
        reason=reason,
    )

    session.add(new_record)
    logger.success(f"Mute record added for user {user_id} in chat {chat_id}")


async def add_ban(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    time: datetime,
    name: str,
    status: str,
    duration: str,
    reason: str = None,
):
    """
    Logs a new ban action to the database history.
    """
    user = await session.get(User, (user_id, chat_id))
    if not user:
        user = User(id=user_id, chat_id=chat_id)
        session.add(user)

    user.count_bans = (user.count_bans or 0) + 1
    user.is_banned = True

    new_record = BanHistory(
        user_id=user_id,
        chat_id=chat_id,
        time=time,
        name=name,
        status=status,
        duration=duration,
        reason=reason,
    )

    session.add(new_record)
    logger.success(f"Ban record added for user {user_id} in chat {chat_id}")


async def unmute_user(session: AsyncSession, user_id: int, chat_id: int):
    """
    Updates the user's status in the database to unmuted.
    """
    user = await session.get(User, (user_id, chat_id))
    if user:
        user.is_muted = False
        logger.info(f"User {user_id} in chat {chat_id} unmuted in database")


async def unban_user(session: AsyncSession, user_id: int, chat_id: int):
    """
    Updates the user's status in the database to unbanned.
    """
    user = await session.get(User, (user_id, chat_id))
    if user:
        user.is_banned = False
        logger.info(f"User {user_id} in chat {chat_id} unbanned in database")


async def set_log_chat(session: AsyncSession, group_id, log_chat_id):
    """
    Configures the chat ID where moderation logs will be sent for a specific group.
    """
    config = await session.get(ChatConfig, group_id)

    if not config:
        config = ChatConfig(group_id=group_id, log_chat_id=log_chat_id)
        session.add(config)
    else:
        config.log_chat_id = log_chat_id

    logger.success(f'Log channel for group {group_id} set to {log_chat_id}')


async def get_log_chat(session: AsyncSession, group_id):
    """
    Retrieves the configured admin log channel ID for a specific group.
    """
    config = await session.get(ChatConfig, group_id)
    return config.log_chat_id if config else None


async def get_ban_list(session: AsyncSession):
    """
    Retrieves all ban history records from the database.
    """
    result = await session.execute(select(BanHistory))
    return result.scalars().all()


async def get_mute_list(session: AsyncSession):
    """
    Retrieves all mute history records from the database.
    """
    result = await session.execute(select(MuteHistory))
    return result.scalars().all()
