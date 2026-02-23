from datetime import datetime
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
                user = await session.get(User, (event.from_user.id, event.chat.id))
                if user:
                    user.count_messages = (user.count_messages or 0) + 1
                else:
                    new_user = User(
                        id=event.from_user.id, 
                        chat_id=event.chat.id, 
                        count_messages=1,
                        join_date=datetime.now()
                    )
                    session.add(new_user)
                
                await session.commit()

        return await handler(event, data)
