from aiogram.filters import Filter
from aiogram import Bot, types

from config.strings import NOT_REPLY_TO_MESSAGE


class IsAdmin(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)

        return True if member.status in ("creator", "administrator") else False


class CanBeRestricted(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        if not message.reply_to_message:
            await message.reply(NOT_REPLY_TO_MESSAGE)
            return False

        target = await bot.get_chat_member(
            chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
        )
        return target.status not in ("creator", "administrator")
