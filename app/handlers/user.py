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

    user = (message.reply_to_message.from_user 
            if message.reply_to_message 
            else message.from_user)

    stats = await get_user_stats(
        session=session, 
        user_id=user.id,
        chat_id=message.chat.id
    )

    await message.reply(
        STATS_TEXT.format(
            user_id=stats["user_id"],
            user_fullname=user.full_name,
            count_messages=stats["count_messages"],
            count_mutes=stats["count_mutes"],
            count_bans=stats["count_bans"],
            count_warns=stats["count_warns"],
            join_date=stats["join_date"],
        )
    )