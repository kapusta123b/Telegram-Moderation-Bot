from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    count_mutes: Mapped[int] = mapped_column(nullable=True, default=0)
    count_warns: Mapped[int] = mapped_column(nullable=True, default=0)

class ChatConfig(Base):
    __tablename__ = 'chatconfig'

    chat_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)