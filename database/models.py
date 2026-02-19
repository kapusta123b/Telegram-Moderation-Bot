from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(primary_key=True)

    count_mutes: Mapped[int] = mapped_column(nullable=True, default=0)
    count_warns: Mapped[int] = mapped_column(nullable=True, default=0)
    count_bans: Mapped[int] = mapped_column(nullable=True, default=0)
    count_messages: Mapped[int] = mapped_column(default=0)

    is_banned: Mapped[bool] = mapped_column(default=False)
    ban_duration: Mapped[datetime] = mapped_column(nullable=True)

    is_muted: Mapped[bool] = mapped_column(default=False)
    mute_duration: Mapped[datetime] = mapped_column(nullable=True)

    join_date: Mapped[datetime] = mapped_column(nullable=True)



class ChatConfig(Base):
    __tablename__ = "chat_config"

    group_id: Mapped[int] = mapped_column(primary_key=True)
    log_chat_id: Mapped[int] = mapped_column(nullable=True)



class BanHistory(Base):
    __tablename__ = "ban_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column()

    time: Mapped[datetime] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(nullable=True)

    duration: Mapped[str] = mapped_column(nullable=True)

    reason: Mapped[str] = mapped_column(nullable=True)



class MuteHistory(Base):
    __tablename__ = "mute_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column()

    time: Mapped[datetime] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(nullable=True)

    duration: Mapped[str] = mapped_column(nullable=True)

    reason: Mapped[str] = mapped_column(nullable=True)



class WarnHistory(Base):
    __tablename__ = "warn_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column()

    time: Mapped[datetime] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(nullable=True)