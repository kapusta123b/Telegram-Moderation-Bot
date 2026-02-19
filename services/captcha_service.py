from datetime import datetime, timedelta

from aiogram import Bot, types

from sqlalchemy.ext.asyncio import AsyncSession

from config.config import permissions_mute, permissions_unmute

from services.log_service import send_log

from loguru import logger


class CaptchaService:
    def __init__(self, bot: Bot, session: AsyncSession):
        self.bot = bot
        self.session = session

    async def restrict_new_user(self, chat_id: int, user_id: int):
        """
        Initializes the captcha process by muting the newly joined user.
        """

        await self.bot.restrict_chat_member(
            chat_id=chat_id, user_id=user_id, permissions=permissions_mute
        )

    async def verify_user(self, chat_id: int, user: types.User):
        """
        Restores member permissions after successful captcha verification.
        """

        await self.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=permissions_unmute,
        )
        logger.info(f"User {user.id} passed captcha in chat {chat_id}")

    async def fail_captcha(self, chat: types.Chat, user: types.User):
        """
        Bans the user for 1 hour if they fail to pass the captcha in time.
        """

        await self.bot.ban_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            until_date=datetime.now() + timedelta(hours=1),
        )

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=chat,
            user=user,
            action="Banned (Captcha Failed)",
            duration="1 hour",
        )
        logger.info(f"User {user.id} failed captcha in chat {chat.id}")