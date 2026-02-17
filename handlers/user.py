from aiogram import Router, types
from aiogram.filters import Command

from sqlalchemy.ext.asyncio import AsyncSession

from config.strings import STATS_TEXT
from database.requests import get_user_stats
from filters.chat_filters import ChatTypeFilter


user_router = Router()
user_router.message.filter(ChatTypeFilter(["group", "supergroup", "private"]))

@user_router.message(Command('stats'))
async def stats_cmd(message: types.Message, session: AsyncSession):
    """
    Get and display user statistics in the current chat.
    """

    stats = await get_user_stats(
        session=session, 
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )

    await message.reply(
        STATS_TEXT.format(
            user_id=stats["user_id"],
            count_mutes=stats["count_mutes"],
            count_bans=stats["count_bans"],
            count_warns=stats["count_warns"],
            join_date=stats["join_date"],
        )
    )