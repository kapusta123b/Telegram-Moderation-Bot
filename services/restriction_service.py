from typing import Literal
from aiogram import types, Bot
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from services.warning_service import get_mute_duration
from database.requests import (
    add_mute,
    add_ban,
    add_warn,
    add_warn_log,
    unmute_user,
    unban_user,
    unwarn_user,
)
from config.config import MAX_WARNS, permissions_mute, permissions_unmute
import config.strings as s

from loguru import logger
from services.log_service import send_log


class AlreadyRestrictedError(Exception):
    pass


class NotRestrictedError(Exception):
    pass


class AlreadyBannedError(Exception):
    pass


class ZeroCurrentWarns(Exception):
    pass


class RestrictionService:
    def __init__(self, bot: Bot, session: AsyncSession):
        self.bot = bot
        self.session = session

    async def _get_target_member(self, chat_id: int, target_id: int):
        """
        Internal helper to retrieve chat member info and verify they aren't an admin.
        """
        target = await self.bot.get_chat_member(chat_id, target_id)
        if target.status in ("administrator", "creator"):
            raise PermissionError("Cannot restrict admin")

        return target

    async def mute(
        self,
        chat_id: int,
        user: types.User,
        until_date: datetime | None,
        reason: str | None,
        extend: bool = False,
        message: types.Message | None = None,
    ):
        """
        Mutes a user in the specified chat and logs the action.
        """
        target = await self._get_target_member(chat_id, user.id)

        is_muted = target.status == "restricted" and not getattr(
            target, "can_send_messages", True
        )

        if is_muted and not extend:
            raise AlreadyRestrictedError

        await self.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=permissions_mute,
            until_date=until_date,
        )

        duration_str = (
            "permanent"
            if until_date is None
            else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
        )

        await add_mute(
            session=self.session,
            user_id=user.id,
            chat_id=chat_id,
            time=datetime.now(),
            name=user.full_name,
            status="Muted",
            duration_str=duration_str,
            until_date=until_date,
            reason=reason,
        )

        action = "Mute" if not extend else "Mute (Update)"
        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action=action,
            duration=duration_str,
            reason=reason,
            message=message,
        )

        return {"status": "muted", "until_date": until_date}

    async def unmute(
        self, chat_id: int, user: types.User, message: types.Message | None = None
    ):
        """
        Restores message permissions for a restricted user.
        """
        target = await self._get_target_member(chat_id, user.id)

        if target.status != "restricted":  # if target not muted
            raise NotRestrictedError

        await self.bot.restrict_chat_member(
            chat_id=chat_id, user_id=user.id, permissions=permissions_unmute
        )

        await unmute_user(self.session, user.id, chat_id)

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action="Unmute",
            message=message,
        )

        return {"status": "unmuted"}

    async def ban(
        self,
        chat_id: int,
        user: types.User,
        until_date: datetime | None,
        reason: str | None,
        extend: bool = False,
        message: types.Message | None = None,
    ):
        """
        Bans a user from the chat and logs the action.
        """
        target = await self._get_target_member(chat_id, user.id)

        if target.status in ("kicked", "left") and not extend:
            raise AlreadyBannedError

        await self.bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            until_date=until_date,
            revoke_messages=True,
        )

        duration_str = (
            "permanent"
            if until_date is None
            else f"until {until_date.strftime('%Y-%m-%d %H:%M')}"
        )

        await add_ban(
            session=self.session,
            user_id=user.id,
            chat_id=chat_id,
            time=datetime.now(),
            name=user.full_name,
            status="Banned",
            duration=duration_str,
            reason=reason,
        )

        action = "Ban" if not extend else "Ban (Update)"

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action=action,
            duration=duration_str,
            reason=reason,
            message=message,
        )

        return {"status": "banned", "until_date": until_date}

    async def unban(
        self, chat_id: int, user: types.User, message: types.Message | None = None
    ):
        """
        Lifts a ban for a user, allowing them to rejoin the chat.
        """
        # we don't check target status here as they might not be in the chat
        await self.bot.unban_chat_member(
            chat_id=chat_id, user_id=user.id, only_if_banned=True
        )

        await unban_user(self.session, user.id, chat_id)

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action="Unban",
            message=message,
        )

        return {"status": "unbanned"}

    async def warn(
        self,
        chat_id: int,
        user: types.User,
        message: types.Message | None = None,
        reason: str | None = None,
    ):
        """
        Issues a warning to a user, with auto-mute triggered after 3 warnings.
        """
        current_warns, mutes = await add_warn(self.session, user.id, chat_id)

        if current_warns < MAX_WARNS:
            logger.info(f"Warning {current_warns}/{MAX_WARNS} issued to {user.id}")

            await send_log(
                bot=self.bot,
                session=self.session,
                chat=message.chat if message else chat_id,
                user=user,
                action=f"Warning ({current_warns}/{MAX_WARNS})",
                reason=reason,
                message=message,
            )

            await add_warn_log(
                session=self.session,
                user_id=user.id,
                chat_id=chat_id,
                time=datetime.now(),
                name=user.full_name,
                status="Warned",
            )

            return {"status": "warned", "current_warns": current_warns}

        duration = get_mute_duration(mutes)
        until_date = datetime.now() + duration

        await self.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=permissions_mute,
            until_date=until_date,
        )

        hours = int(duration.total_seconds() // 3600)
        days = hours // 24
        duration_str = f"{days} days" if days > 0 else f"{hours} hours"

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action=f"Auto-Mute ({MAX_WARNS}/{MAX_WARNS} Warnings)",
            duration=duration_str,
            message=message,
        )

        return {
            "status": "auto_muted",
            "current_warns": current_warns,
            "duration": duration_str,
            "mute_count": mutes,
            "until_date": until_date,
        }

    async def unwarn(
        self,
        chat_id: int,
        user: types.User,
        message: types.Message | None = None,
    ):

        current_warns = await unwarn_user(
            self.session, user_id=user.id, chat_id=chat_id
        )

        if current_warns < 0:
            raise ZeroCurrentWarns

        await send_log(
            bot=self.bot,
            session=self.session,
            chat=message.chat if message else chat_id,
            user=user,
            action=f"Unwarn",
            duration=None,
            message=message,
        )

        return {"status": "unwarned", "current_warns": current_warns}
