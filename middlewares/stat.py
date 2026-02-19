from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import update
from database.models import User

class MessageCounterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message) and event.from_user and not event.from_user.is_bot:
            session = data.get("session")
            if session:
                await session.execute(
                    update(User)
                    .where(
                        User.id == event.from_user.id, 
                        User.chat_id == event.chat.id
                    )
                    .values(count_messages=User.count_messages + 1)
                )
                await session.commit()

        return await handler(event, data)
