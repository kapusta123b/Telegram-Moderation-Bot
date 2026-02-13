from aiogram import types, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from database.requests import (
    get_ban_list,
    get_mute_list,
)
from filters.group_filters import IsAdmin
from filters.chat_filters import ChatTypeFilter

lists_router = Router()
lists_router.message.filter(ChatTypeFilter(["group", "supergroup"]))

@lists_router.message(Command("ban_list"), IsAdmin())
async def ban_list_cmd(message: types.Message, command: CommandObject, session: AsyncSession):
    """
    The handler sends a list of baned users
    """

    # returns a list of users who have ever been baned
    bans = await get_ban_list(session)

    if not bans:
        await message.reply(s.BAN_NO_RECORDS)
        return
    
    # if arguments are passed, it takes the first argument (the number of users to be displayed), otherwise 0
    number_of_users = int(command.args.split()[0]) if command.args else 0

    history_scope = (
        f"{number_of_users} <b>Users</b>"
        if number_of_users
        else "Full history"
    )

    text = s.BAN_HISTORY_HEADER.format(history_scope=history_scope)

    for ban in bans[-number_of_users:]: # the number of users is taken depending on the number in number_of_users
        date_str = ban.time.strftime("%Y-%m-%d %H:%M") # formatting into a convenient form

        reason_text = ban.reason if ban.reason else "None"

        text += s.LIST_RECORD.format(
            name=ban.name,
            user_id=ban.user_id,
            date=date_str,
            duration=ban.duration,
            reason=reason_text,
        )

    await message.reply(text)


@lists_router.message(Command("mute_list"), IsAdmin())
async def mute_list_cmd(message: types.Message, session: AsyncSession, command: CommandObject):
    """
    The handler sends a list of muted users
    """
    
    # returns a list of users who have ever been muted
    mutes = await get_mute_list(session)

    if not mutes:
        await message.reply(s.MUTE_NO_RECORDS)
        return

    # if arguments are passed, it takes the first argument (the number of users to be displayed), otherwise 0
    number_of_users = int(command.args.split()[0]) if command.args else 0
    
    history_scope = (
        f"{number_of_users} <b>Users</b>"
        if number_of_users
        else "Full history"
    )

    text = s.MUTE_HISTORY_HEADER.format(history_scope=history_scope)

    for mute in mutes[-number_of_users:]: # the number of users is taken depending on the number in number_of_users
        date_str = mute.time.strftime("%Y-%m-%d %H:%M") # formatting into a convenient form
        
        reason_text = mute.reason if mute.reason else "None"

        text += s.LIST_RECORD.format(
            name=mute.name,
            user_id=mute.user_id,
            date=date_str,
            duration=mute.duration,
            reason=reason_text,
        )

    await message.reply(text)
