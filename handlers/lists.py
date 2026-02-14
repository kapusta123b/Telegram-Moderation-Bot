from aiogram import F, Bot, types, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

import config.strings as s
from filters.group_filters import IsAdmin
from filters.chat_filters import ChatTypeFilter
from services.history_service import HistoryService, NoRecordsBan, NoRecordsMute, Pagination

lists_router = Router()
lists_router.message.filter(ChatTypeFilter(["group", "supergroup"]))

def get_pagination_kb(action: str, page: int, has_next: bool, has_prev: bool):
    """Navigation button generator"""

    builder = InlineKeyboardBuilder()
    
    if has_prev:
        builder.button(text="⬅️ Назад", callback_data=Pagination(action=action, page=page-1))
    
    if has_next:
        builder.button(text="Вперед ➡️", callback_data=Pagination(action=action, page=page+1))
    
    return builder.as_markup()


@lists_router.message(Command("ban_list", "mute_list"), IsAdmin())
async def list_cmd(message: types.Message, session: AsyncSession, command: CommandObject):
    """The main handler for the /ban_list and /mute_list commands"""
    
    action = command.command

    services = HistoryService(session=session, history_scope="Full history")
    
    try:
        if action == 'ban_list':
            result = await services.ban_history(page=1)
        else:
            result = await services.mute_history(page=1)
            
    except NoRecordsBan:
        return await message.reply(s.BAN_NO_RECORDS)
    
    except NoRecordsMute:
        return await message.reply(s.MUTE_NO_RECORDS)

    await message.reply(
        text=result["text"],
        reply_markup=get_pagination_kb(
            action=action, 
            page=1, 
            has_next=result["has_next"], 
            has_prev=result["has_prev"]
        )
    )


@lists_router.callback_query(Pagination.filter())
async def list_pagination_handler(callback: types.CallbackQuery, callback_data: Pagination, session: AsyncSession):
    """Handler for pressing the Forward/Backward buttons"""
    
    services = HistoryService(session=session, history_scope="Full history")
    
    if callback_data.action == 'ban_list':
        result = await services.ban_history(page=callback_data.page)
    else:
        result = await services.mute_history(page=callback_data.page)
    
    await callback.message.edit_text(
        text=result["text"],
        reply_markup=get_pagination_kb(
            action=callback_data.action, 
            page=callback_data.page, 
            has_next=result["has_next"], 
            has_prev=result["has_prev"]
        )
    )

    await callback.answer()