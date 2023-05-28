from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column as col
from sqlalchemy.types import BIGINT, BOOLEAN, INTEGER


class Base(AsyncAttrs, DeclarativeBase):
    pass


@dataclass
class User(Base):
    __tablename__ = "bot_users"

    qq: Mapped[int] = col(
        BIGINT(), nullable=False, index=True, unique=True, primary_key=True
    )
    favor: Mapped[int] = col(INTEGER(), nullable=False, default=20, comment="好感度")
    days: Mapped[int] = col(INTEGER(), nullable=False, default=0, comment="签到总天数")
    today: Mapped[bool] = col(BOOLEAN(), nullable=False, default=False, comment='今日是否签到')
