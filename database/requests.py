from datetime import datetime

from database.models import BanHistory, MuteHistory, User, ChatConfig

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_user(session: AsyncSession, user_id):
    user = await session.get(User, user_id)

    if not user:
        new_user = User(id=user_id)
        session.add(new_user)
        await session.commit()


async def add_warn(session: AsyncSession, user_id):
    user = await session.get(User, user_id)

    if not user:
        user = User(id=user_id, count_warns=1)
        session.add(user)
    else:
        user.count_warns += 1

    current_warns = user.count_warns

    if user.count_warns >= 3:
        user.count_warns = 0
        user.count_mutes += 1
        user.is_muted = True

    mutes = user.count_mutes

    await session.commit()

    return current_warns, mutes


async def add_mute(
    session: AsyncSession,
    user_id: int,
    time: datetime,
    name: str,
    status: str,
    duration: str,
    reason: str = None,
):
    user = await session.get(User, user_id)
    if not user:
        user = User(id=user_id)
        session.add(user)

    user.count_mutes += 1
    user.is_muted = True

    new_record = MuteHistory(
        user_id=user_id,
        time=time,
        name=name,
        status=status,
        duration=duration,
        reason=reason,
    )

    session.add(new_record)

    await session.commit()


async def add_ban(
    session: AsyncSession,
    user_id: int,
    time: datetime,
    name: str,
    status: str,
    duration: str,
    reason: str = None,
):
    user = await session.get(User, user_id)
    if not user:
        user = User(id=user_id)
        session.add(user)

    user.count_bans += 1
    user.is_banned = True

    new_record = BanHistory(
        user_id=user_id,
        time=time,
        name=name,
        status=status,
        duration=duration,
        reason=reason,
    )

    session.add(new_record)

    await session.commit()


async def set_log_chat(session: AsyncSession, log_chat_id):
    log_chat = await session.get(ChatConfig, log_chat_id)

    if not log_chat:
        log_chat = ChatConfig(chat_id=log_chat_id)
        session.add(log_chat)

    elif log_chat.chat_id == log_chat_id:
        raise ValueError

    else:
        log_chat.chat_id = log_chat_id

    await session.commit()


async def get_log_chat(session: AsyncSession):
    result = await session.execute(select(ChatConfig))

    config = result.scalars().first()

    return config.chat_id if config else None


async def get_ban_list(session: AsyncSession):
    result = await session.execute(select(BanHistory))
    return result.scalars().all()


async def get_mute_list(session: AsyncSession):
    result = await session.execute(select(MuteHistory))
    return result.scalars().all()