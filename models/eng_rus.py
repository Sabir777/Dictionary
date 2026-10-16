from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


user_group = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)
