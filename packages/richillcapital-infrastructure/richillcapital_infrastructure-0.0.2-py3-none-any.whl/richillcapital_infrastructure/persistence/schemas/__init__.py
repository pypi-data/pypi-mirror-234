from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """ """


class TradingApp(Base):
    """ """

    __tablename__ = "trading_apps"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text())
    category: Mapped[str] = mapped_column(String(12))
    platform: Mapped[str] = mapped_column(String(12))


class Work(Base):
    """ """

    __tablename__ = "works"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    specification: Mapped[str] = mapped_column(String(128))
    budget: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(128))
    user_id: Mapped[str] = mapped_column(String(128))
