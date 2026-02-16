from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from services.log_service import send_log
from filters.chat_filters import ChatTypeFilter

reports_router = Router()
reports_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@reports_router.message(Command("report"))
async def report_cmd(
    message: types.Message, command: CommandObject, bot: Bot, session: AsyncSession
):
    """
    This handler sends a log as a report to the admin channel.
    """

    if message.reply_to_message:
        target_user = message.reply_to_message.from_user

        reporter = message.from_user

        reason = command.args if command.args else "No reason provided"

        await send_log(
            bot=bot,
            session=session,
            chat=message.chat,
            user=target_user,
            action=f"Reported by {reporter.first_name}",
            message=message.reply_to_message,
            reason=reason,
        )

        await message.reply(s.REPORT_SENT)

    else:
        await message.reply(s.REPORT_NO_REPLY)
