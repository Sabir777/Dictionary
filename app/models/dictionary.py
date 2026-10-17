from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from base import Base


class Translate(Base):
    __tablename__ = "eng_rus"

    id: Mapped[int] = mapped_column(prymary_key=True)
    word: Mapped[str] = mapped_column(Text)
    value: Mapped[str] = mapped_column(Text)
    context_en: Mapped = mapped_column(Text)
    context_ru: Mapped[str] = mapped_column(Text)
    comment: Mapped[str] = mapped_column(Text)
