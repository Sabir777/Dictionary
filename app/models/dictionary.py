from models import Base
from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Context(Base):
    __tablename__ = "contexts"

    id: Mapped[int] = mapped_column(primary_key=True)
    context_en: Mapped[str] = mapped_column(Text, nullable=False)
    context_ru: Mapped[str] = mapped_column(Text, nullable=False)

    translations: Mapped[list["Dictionary"]] = relationship(back_populates="context")

    __table_args__ = (
        UniqueConstraint("context_en", "context_ru", name="uq_contexts_en_ru"),
    )

    def __repr__(self) -> str:
        return f"Context(id={self.id!r}, context_en={self.context_en!r}, context_ru={self.context_ru!r})"


class Dictionary(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    context_id: Mapped[int] = mapped_column(ForeignKey("contexts.id"), nullable=True)

    context: Mapped["Context"] = relationship(back_populates="translations")

    __table_args__ = (
        UniqueConstraint("word", "value", name="uq_translates_word_value"),
    )

    def __repr__(self) -> str:
        return f"Translate(id={self.id!r}, word={self.word!r}, value={self.value!r})"
