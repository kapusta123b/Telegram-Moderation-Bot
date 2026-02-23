from datetime import datetime

from config.config import MAX_WARNS
from database.models import BanHistory, MuteHistory, User, ChatConfig, WarnHistory

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from loguru import logger


async def create_user(session: AsyncSession, user_id: int | None, chat_id: int | None):
    """
    Ensures a user exists in the database. Creates a new record if not found.
    """
    
    user = await session.get(User, (user_id, chat_id))

    if not user:
        new_user = User(id=user_id, chat_id=chat_id, join_date=datetime.now())
        session.add(new_user)
        logger.info(f"New user {user_id} in chat {chat_id} created in database")


async def get_user_stats(session: AsyncSession, user_id: int | None, chat_id: int | None):
    """
    Returns all user statistics for being in the chat.
    If the user doesn't exist, returns default zero stats.
    """

    stats = await session.get(User, (user_id, chat_id))

    if not stats:
        return {
            'user_id': user_id,
            'count_mutes': 0,
            'count_bans': 0,
            'count_warns': 0,
            'join_date': 'N/A',
            'count_messages': 0
        }

    return {
        'user_id': stats.id,
        'count_mutes': stats.count_mutes or 0,
        'count_bans': stats.count_bans or 0,
        'count_warns': stats.count_warns or 0,
        'join_date': stats.join_date.strftime('%Y-%m-%d %H:%M') if stats.join_date else 'N/A',
        'count_messages': stats.count_messages or 0
    }


async def add_warn(session: AsyncSession, user_id: int, chat_id: int):
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
    duration_str: str,
    until_date: datetime | None,
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
    user.mute_duration = until_date

    new_record = MuteHistory(
        user_id=user_id,
        chat_id=chat_id,
        time=time,
        name=name,
        status=status,
        duration=duration_str,
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
    until_date: datetime | None,
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
    user.ban_duration = until_date

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


async def add_warn_log(
    session: AsyncSession,
    user_id: int,
    chat_id: int,
    time: datetime,
    name: str,
    status: str,
):
    """
    Logs a new warn action to the database history.
    """

    user = await session.get(User, (user_id, chat_id))
    if not user:
        user = User(id=user_id, chat_id=chat_id)
        session.add(user)

    new_record = WarnHistory(
        user_id=user_id,
        chat_id=chat_id,
        time=time,
        name=name,
        status=status,
    )

    session.add(new_record)
    logger.success(f"Warn record added for user {user_id} in chat {chat_id}")


async def unmute_user(session: AsyncSession, user_id: int, chat_id: int):
    """
    Updates the user's status in the database to unmuted.
    """

    user = await session.get(User, (user_id, chat_id))
    if user:
        user.is_muted = False
        user.mute_duration = None

        logger.info(f"User {user_id} in chat {chat_id} unmuted in database")


async def unban_user(session: AsyncSession, user_id: int, chat_id: int):
    """
    Updates the user's status in the database to unbanned.
    """

    user = await session.get(User, (user_id, chat_id))
    if user:
        user.is_banned = False
        user.ban_duration = None

        logger.info(f"User {user_id} in chat {chat_id} unbanned in database")


async def unwarn_user(session: AsyncSession, user_id: int, chat_id: int):
    """
    Decrements the user's warning count in the database.
    """

    user = await session.get(User, (user_id, chat_id))
    if not user or user.count_warns <= 0:
        return -1

    user.count_warns -= 1
    logger.info(f"User {user_id} in chat {chat_id} -1 warn in database")
    return user.count_warns


async def set_log_chat(session: AsyncSession, group_id, log_chat_id):
    """
    Configures the chat ID where moderation logs will be sent for a specific group.
    """

    config = await session.get(ChatConfig, group_id)

    if not config:
        config = ChatConfig(group_id=group_id, log_chat_id=log_chat_id)
        session.add(config)
    else:
        if config.log_chat_id == log_chat_id:
            raise ValueError("Already configured for this chat")
        config.log_chat_id = log_chat_id

    logger.success(f"Log channel for group {group_id} set to {log_chat_id}")


async def unset_log_chat(session: AsyncSession, group_id):
    """
    Removes the log chat configuration for a specific group.
    """

    config = await session.get(ChatConfig, group_id)

    if config:
        await session.delete(config)

    else:
        raise ValueError("Log chat not configured")

    logger.success(f"Log channel for group {group_id} unset")


async def get_log_chat(session: AsyncSession, group_id):
    """
    Retrieves the configured admin log channel ID for a specific group.
    """

    config = await session.get(ChatConfig, group_id)
    return config.log_chat_id if config else None


async def get_history_list(
    session: AsyncSession,
    model,
    current: bool,
    status: str | None,
):
    """
    Retrieves a list of records from the specified history model.
    Optionally filters for currently active restrictions.
    """

    query = select(model)

    if current and status:
        duration_field = (
            User.mute_duration if status == "is_muted" else User.ban_duration
        )
        query = query.join(
            User, (model.user_id == User.id) & (model.chat_id == User.chat_id)
        ).where(
            getattr(User, status) == True,
            or_(duration_field == None, duration_field > datetime.now()),
        )

    result = await session.execute(query)
    return result.scalars().all()
