from aiogram import Bot, types
from aiogram.filters import Filter


class IsAdmin(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)

        return member.status in ("creator", "administrator")
