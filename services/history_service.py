import math
from html import escape
from typing import Callable
from aiogram.filters.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from config.strings import BAN_HISTORY_HEADER, MUTE_HISTORY_HEADER, LIST_RECORD
from database.requests import get_ban_list, get_mute_list

class NoRecordsBan(Exception):
    pass

class NoRecordsMute(Exception):
    pass

class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int

class HistoryService:
    def __init__(self, session: AsyncSession, history_scope: str):
        self.session = session
        self.history_scope = history_scope

    async def _get_formatted_history(self, fetch_func: Callable, header: str, exception_class: Exception, page: int = 1):
        records = await fetch_func(session=self.session)

        if not records:
            raise exception_class

        records = sorted(records, key=lambda x: x.time, reverse=True)

        PER_PAGE = 10 
        total_pages = math.ceil(len(records) / PER_PAGE)
        
        start = (page - 1) * PER_PAGE
        end = start + PER_PAGE
        page_records = records[start:end]

        text = header.format(history_scope=self.history_scope)

        for record in page_records:
            date = record.time.strftime("%Y-%m-%d %H:%M")
            reason_text = escape(record.reason) if record.reason else "None"
            name_text = escape(record.name) if record.name else "Unknown"

            text += LIST_RECORD.format(
                name=name_text,
                user_id=record.user_id,
                date=date,
                duration=record.duration,
                reason=reason_text,
            )

        return {
            "text": text,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "total_pages": total_pages
        }

    async def ban_history(self, page: int = 1):
        return await self._get_formatted_history(get_ban_list, BAN_HISTORY_HEADER, NoRecordsBan, page)

    async def mute_history(self, page: int = 1):
        return await self._get_formatted_history(get_mute_list, MUTE_HISTORY_HEADER, NoRecordsMute, page)
