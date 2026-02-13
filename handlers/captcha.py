from asyncio import sleep
from datetime import datetime, timedelta

from aiogram import types, Router, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from config.config import permissions_mute, permissions_unmute
from services.log_service import send_log
from filters.chat_filters import ChatTypeFilter

from loguru import logger

captcha_router = Router()
captcha_router.message.filter(ChatTypeFilter(["group", "supergroup"]))

@captcha_router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def captcha(event: types.ChatMemberUpdated, session: AsyncSession):
    """
    This handler automatically mutes the user when they join until they press the button.
    """

    user_id = event.new_chat_member.user.id

    await event.bot.restrict_chat_member(
        chat_id=event.chat.id, user_id=user_id, permissions=permissions_mute
    )

    builder = InlineKeyboardBuilder().add(
        types.InlineKeyboardButton(
            text="✅ I'm not a robot!", callback_data=f"not_bot:{user_id}"
        )
    )

    captcha_msg = await event.bot.send_message(
        chat_id=event.chat.id,
        text=s.VERIFICATION_TEXT.format(first_name=event.new_chat_member.user.first_name),
        reply_markup=builder.as_markup(),
    )

    await sleep(300)

    current_member = await event.bot.get_chat_member(
        chat_id=event.chat.id, user_id=user_id
    )

    if (
        current_member.status == "restricted" and not current_member.can_send_messages
    ) or current_member.status in ("left", "kicked"):
        logger.info(f"User {user_id} failed captcha in chat {event.chat.id}")
        await send_log(
            bot=event.bot,
            session=session,
            chat=event.chat,
            user=event.new_chat_member.user,
            action="Banned (Captcha Failed)",
            duration="24 hours",
        )

        await event.bot.send_message(
            chat_id=event.chat.id,
            text=s.VERIFICATION_FAILED.format(first_name=event.new_chat_member.user.first_name),
        )

        await event.bot.ban_chat_member(
            chat_id=event.chat.id,
            user_id=user_id,
            until_date=datetime.now() + timedelta(days=1),
        )

        try:
            await captcha_msg.delete()

        except Exception:
            logger.debug(f"Could not delete captcha message in chat {event.chat.id}")


@captcha_router.callback_query(F.data.startswith("not_bot:"))
async def captcha_unmute(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split(":")[1])

    if callback.from_user.id == target_user_id:
        logger.info(f"User {target_user_id} successfully passed captcha in chat {callback.message.chat.id}")
        await callback.bot.restrict_chat_member(
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id,
            permissions=permissions_unmute,
        )

        await callback.answer(
            text=s.VERIFICATION_SUCCESS, show_alert=True
        )

        await callback.message.delete()

    else:
        await callback.answer(s.VERIFICATION_NOT_FOR_YOU, show_alert=True)
        return
