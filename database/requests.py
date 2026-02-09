from database.models import User, ChatConfig

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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

    mutes = user.count_mutes

    await session.commit()
    return current_warns, mutes

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

