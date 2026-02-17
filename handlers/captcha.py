from asyncio import sleep

from aiogram import types, Router, F
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s

from services.captcha_service import CaptchaService

from filters.chat_filters import ChatTypeFilter

captcha_router = Router()
captcha_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@captcha_router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION)
)
async def captcha(event: types.ChatMemberUpdated, session: AsyncSession):
    user = event.new_chat_member.user
    service = CaptchaService(event.bot, session)

    await service.restrict_new_user(event.chat.id, user.id)

    builder = InlineKeyboardBuilder().add(
        types.InlineKeyboardButton(
            text="✅ I'm not a robot!", callback_data=f"not_bot:{user.id}"
        )
    )

    captcha_msg = await event.bot.send_message(
        chat_id=event.chat.id,
        text=s.VERIFICATION_TEXT.format(first_name=user.first_name),
        reply_markup=builder.as_markup(),
    )

    await sleep(300)

    current_member = await event.bot.get_chat_member(
        chat_id=event.chat.id, user_id=user.id
    )

    if current_member.status == "restricted" and not current_member.can_send_messages:
        await service.fail_captcha(event.chat, user)

        await event.bot.send_message(
            chat_id=event.chat.id,
            text=s.VERIFICATION_FAILED.format(first_name=user.first_name),
        )

        try:
            await captcha_msg.delete()
        except Exception:
            pass


@captcha_router.callback_query(F.data.startswith("not_bot:"))
async def captcha_unmute(callback: types.CallbackQuery, session: AsyncSession):
    target_user_id = int(callback.data.split(":")[1])

    if callback.from_user.id != target_user_id:
        await callback.answer(s.VERIFICATION_NOT_FOR_YOU, show_alert=True)
        return

    service = CaptchaService(callback.bot, session)
    await service.verify_user(callback.message.chat.id, callback.from_user)

    await callback.answer(text=s.VERIFICATION_SUCCESS, show_alert=True)
    await callback.message.delete()
