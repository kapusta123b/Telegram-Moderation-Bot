from database.models import User

from sqlalchemy.ext.asyncio import AsyncSession

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

