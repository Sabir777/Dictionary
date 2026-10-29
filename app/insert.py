import sys

from db import engine
from insert import CONTEXT_ID, pairs
from models import Context, Dictionary
from sqlalchemy import event
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class ContextNotFoundError(Exception):
    """Контекст с указанным id не найден в таблице contexts."""

    def __init__(self, context_id: int) -> None:
        self.context_id = context_id
        super().__init__(f"Контекст с id={context_id} не найден")


def check_context(session: Session, context_id: int | None) -> None:
    """Проверяет, что контекст существует. Для None ничего не делает."""
    if context_id is None:
        return
    if session.get(Context, context_id) is None:
        raise ContextNotFoundError(context_id)


def insert_translations(
    session: Session, pairs: list[tuple[str, str, str | None]], context_id: int | None
) -> int:
    rows = [
        {"word": w, "value": v, "comment": c, "context_id": context_id}
        for w, v, c in pairs
    ]
    stmt = sqlite_insert(Dictionary).on_conflict_do_nothing(
        index_elements=["word", "value"]
    )
    result = session.connection().execute(stmt, rows)
    return result.rowcount


if __name__ == "__main__":
    with Session(engine) as session:
        try:
            check_context(session, CONTEXT_ID)
            inserted = insert_translations(session, pairs, CONTEXT_ID)
            session.commit()
        except ContextNotFoundError:
            print("Передан несуществующий контекст")
            sys.exit(1)
        except SQLAlchemyError:
            session.rollback()
            raise
        else:
            print(
                f"Добавлено: {inserted} из {len(pairs)}, "
                f"пропущено (не добавлено из-за конфликта): {len(pairs) - inserted}"
            )
