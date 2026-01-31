from database.models import User

from sqlalchemy.ext.asyncio import AsyncSession

async def add_warn(session: AsyncSession, user_id):
    user = await session.get(User, user_id)

    if not user:
        user = User(id=user_id)
        session.add(user)
    else:
        user.count_warns += 1

    warns = user.count_warns
    mutes = user.count_mutes

    if user.count_warns >= 3:
        user.count_warns = 0
        user.count_mutes += 1

    await session.commit()
    return warns, user.count_mutes

