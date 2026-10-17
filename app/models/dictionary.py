from base import Base
from sqlalchemy import Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Translate(Base):
    __tablename__ = "translates"

    id: Mapped[int] = mapped_column(prymary_key=True)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    context_en: Mapped[str] = mapped_column(Text, nullable=True)
    context_ru: Mapped[str] = mapped_column(Text, nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (UniqueConstraint("word", "value", name="uq_translates_word_value"),)
