from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = "chat"
    id: Mapped [int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped [int]
    request: Mapped[str]
    response: Mapped [str]