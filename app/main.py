import readline  # noqa: F401

from db import engine, init_db
from models import Context, Dictionary
from rich.console import Console
from rich.table import Table
from sqlalchemy import Row, String, inspect, select  # noqa: F401
from sqlalchemy.orm import Session


def add_translate(**kwargs) -> None:
    """Добавить перeвод в базу данных"""
    kwargs2 = {k.lower(): v for k, v in kwargs.items() if v}
    with Session(engine) as session:
        session.add(Dictionary(**kwargs2))
        session.commit()

def add_context(context_en, context_ru) -> None:
    """Добавить контекст в базу данных"""
    with Session(engine) as session:
        session.add(Context(context_en=context_en, context_ru=context_ru))
        session.commit()

# def add_translate_dict(translates: dict) -> None:
#     """Добавить переводы в базу данных"""
#     with Session(engine) as session:
#         dict_list = [Dictionary(word=w, value=v) for w, v in translates.items()]
#         session.add_all(dict_list)
#         session.commit()


def get_translate_en_to_ru(_word: str):
    """Получить перевод с английского на русский (outer join с contexts).

    Возвращает строки как будто из одной «плоской» таблицы с полями:
    id, word, value, context_en, context_ru, comment.
    Если у перевода нет контекста, context_en/context_ru будут NULL (outer join).
    """
    with Session(engine) as session:
        stmt = (
            select(
                Dictionary.id,
                Dictionary.word,
                Dictionary.value,
                Context.context_en,
                Context.context_ru,
                Dictionary.comment,
            )
            .outerjoin(Context, Dictionary.context)
            .where(Dictionary.word.ilike(f"%{_word}%"))
        )
        return session.execute(stmt).all()


def get_translate_ru_to_en(_word: str):
    """Получить перевод c русского на английский (outer join с contexts).

    Возвращает строки как будто из одной «плоской» таблицы с полями:
    id, word, value, context_en, context_ru, comment.
    Если у перевода нет контекста, context_en/context_ru будут NULL (outer join).
    """
    with Session(engine) as session:
        stmt = (
            select(
                Dictionary.id,
                Dictionary.word,
                Dictionary.value,
                Context.context_en,
                Context.context_ru,
                Dictionary.comment,
            )
            .outerjoin(Context, Dictionary.context)
            .where(Dictionary.value.ilike(f"%{_word}%"))
        )
        return session.execute(stmt).all()

def get_context(_word: str):
    """Получить один или несколько контекстов по ключевому слову"""
    with Session(engine) as session:
        return session.scalars(
            select(Context).where(Context.context_en.ilike(f"%{_word}%"))
        ).all()

def print_translate(title: str, v: Row) -> None:
    """Напечатать перевод.

    `v` — строка-результат запроса с outer join: поля
    id, word, value, context_en, context_ru, comment.
    """

    H = "bold white on blue"
    H1 = "bold white on yellow"
    H2 = "bold white on magenta"
    H3 = "bold white on green"
    H4 = "bold white on cyan"
    H5 = "bold white on bright_black"

    table = Table(title=title, show_lines=True, header_style=H)
    table.add_column("ID", justify="center")
    table.add_row(str(v.id))
    table.add_row("Word", style=H1)
    table.add_row(v.word)
    table.add_row("Перевод", style=H2)
    table.add_row(v.value)
    if v.context_en:
        table.add_row("Context", style=H3)
        table.add_row(v.context_en)
    if v.context_ru:
        table.add_row("Контекст", style=H4)
        table.add_row(v.context_ru)
    if v.comment:
        table.add_row("Комментарий", style=H5)
        table.add_row(v.comment)
    print()
    Console().print(table)

def print_context(title: str, v: Context) -> None:
    """Напечатать контекст"""

    H = "bold white on blue"
    H1 = "bold white on yellow"
    H2 = "bold white on magenta"

    table = Table(title=title, show_lines=True, header_style=H)
    table.add_column("ID", justify="center")
    table.add_row(str(v.id))
    table.add_row("Context: en", style=H1)
    table.add_row(v.context_en)
    table.add_row("Context: ru", style=H2)
    table.add_row(v.context_ru)
    print()
    Console().print(table)

# def normal_to_all_lower() -> None:
#     """Нормализация: перевод всех строковых полей в нижний регистр"""
#     str_cols = [
#         c.key
#         for c in inspect(Dictionary).columns
#         if isinstance(c.type, String) and not c.primary_key
#     ]
#     with Session(engine) as session:
#         for row in session.scalars(select(Dictionary)):
#             for name in str_cols:
#                 value = getattr(row, name)
#                 if value is not None:
#                     setattr(row, name, value.lower())
#         session.commit()


if __name__ == "__main__":
    init_db()  # создать таблицы

    print("""Переключение режимов работы:
    s - выполнить перевод c английского на русский
    sr - выполнить перевод c русского на английский
    sc - показать один или несколько контекстов по ключевому слову
    a - добавить новый перевод
    ac - добавить новый контекст
    u - редактировать перевод
    uc - редактировать контекст
    d - удалить перевод
    dc - удалить контекст
    q - выход из программы""")

    var = "s"
    while var != "q":
        match var:
            case "s":
                while True:
                    print("================================")
                    print("Перевод с английского на русский")
                    var = input("Введите слово: ").strip()
                    if var in ("sr", "a", "u", "d", "q", "ac", "uc", "sc", "dc"):
                        break

                    # Получить переводы с английского на русский
                    result = get_translate_en_to_ru(var)

                    if not result:
                        print("Слово не найдено")
                        continue
                    else:
                        for i, v in enumerate(result):
                            print_translate(str(i + 1), v)
            case "sr":
                while True:
                    print("================================")
                    print("Перевод с русского на английский")
                    var = input("Введите слово: ").strip()
                    if var in ("s", "a", "u", "d", "q", "ac", "uc", "sc", "dc"):
                        break

                    # Получить переводы с русского на английский
                    result = get_translate_ru_to_en(var)

                    if not result:
                        print("Слово не найдено")
                        continue
                    else:
                        for i, v in enumerate(result):
                            print_translate(str(i + 1), v)
            case "sc":
                while True:
                    print("================================")
                    print("Получить контексты по ключевому слову")
                    var = input("Введите слово: ").strip()
                    if var in ("s", "a", "u", "d", "q", "ac", "uc", "sr", "dc"):
                        break

                    # Получить контексты
                    result = get_context(var)

                    if not result:
                        print("Слово не найдено")
                        continue
                    else:
                        for i, v in enumerate(result):
                            print_context(str(i + 1), v)
            case "a":
                while True:
                    print("================================")
                    print("Добавить перевод")
                    var = input("Введите слово: ").strip()
                    if var in ("sr", "s", "u", "d", "q", "ac", "uc", "sc", "dc"):
                        break
                    value = input("Введите перевод: ").strip()
                    context = input("Введите ID контекста: ")
                    context = int(context) if context.isdigit() else None
                    comment = input("Введите комментарий: ").strip().lower()
                    add_translate(
                        word=var,
                        value=value,
                        context=context,
                        comment=comment
                    )
            case "ac":
                while True:
                    print("================================")
                    print("Добавить контекст")
                    var = input("Введите контекст: ").strip()
                    if var in ("sr", "s", "u", "d", "q", "a", "uc", "sc", "dc"):
                        break
                    value = input("Введите перевод контекста: ").strip()
                    if var and value:
                        add_context(context_en=var, context_ru=value)
            case "u":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "d", "q", "ac", "uc", "sc", "dc"):
                        break
                    print("u - пусто")
            case "uc":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "d", "q", "ac", "u", "sc", "dc"):
                        break
                    print("u - пусто")
            case "d":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "u", "q", "ac", "uc", "sc", "dc"):
                        break
                    print("d - пусто")
            case "dс":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "u", "q", "ac", "uc", "sc", "d"):
                        break
                    print("d - пусто")

    # Выход из программы
    table = Table(title="")
    table.add_column("Выход из программы", justify="center")
    table.add_row("До встречи 🤚")
    Console().print(table)
