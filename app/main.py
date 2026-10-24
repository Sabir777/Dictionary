import readline  # noqa: F401

from db import engine, init_db
from models import Dictionary
from rich.console import Console
from rich.table import Table
from sqlalchemy import String, inspect, select
from sqlalchemy.orm import Session


def add_translate(word: str, value: str):
    """Добавить перeвод в базу данных"""
    with Session(engine) as session:
        session.add(Dictionary(word=word, value=value))
        session.commit()


def add_translate_dict(translates: dict):
    """Добавить переводы в базу данных"""
    with Session(engine) as session:
        dict_list = [Dictionary(word=w, value=v) for w, v in translates.items()]
        session.add_all(dict_list)
        session.commit()


def get_translate_en_to_ru(_word: str):
    """Получить перевод с английского на русский"""
    with Session(engine) as session:
        return session.scalars(
            select(Dictionary).where(Dictionary.word.ilike(f"%{_word}%"))
        ).all()


def get_translate_ru_to_en(_word: str):
    """Получить перевод c русского на английский"""
    with Session(engine) as session:
        return session.scalars(
            select(Dictionary).where(Dictionary.value.ilike(f"%{_word}%"))
        ).all()


def print_translate(title: str, v: Dictionary) -> None:
    """Напечатать перевод"""

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


def normal_to_all_lower() -> None:
    """Перевод всех строковых полей в нижний регистр"""
    str_cols = [
        c.key
        for c in inspect(Dictionary).columns
        if isinstance(c.type, String) and not c.primary_key
    ]
    with Session(engine) as session:
        for row in session.scalars(select(Dictionary)):
            for name in str_cols:
                value = getattr(row, name)
                if value is not None:
                    setattr(row, name, value.lower())
        session.commit()


if __name__ == "__main__":
    init_db()  # создать таблицы

# normal_to_all_lower()


# print("""Переключение режимов работы:
# s - выполнить перевод c английского на русский
# sr - выполнить перевод c русского на английский
# a - добавить новый перевод
# u - редактировать перевод
# d - удалить перевод
# q - выход из программы""")

# var = "s"
# while var != "q":
# match var:
# case "s":
# while True:
# print("================================")
# print("Перевод с английского на русский")
# var = input("Введите слово: ").strip()
# if var in ("sr", "a", "u", "d", "q"):
# break

# # Получить переводы с английского на русский
# result = get_translate_en_to_ru(var)

# if not result:
# print("Слово не найдено")
# continue
# else:
# for i, v in enumerate(result):
# print_translate(str(i + 1), v)
# case "sr":
# while True:
# print("================================")
# print("Перевод с русского на английский")
# var = input("Введите слово: ").strip()
# if var in ("s", "a", "u", "d", "q"):
# break

# # Получить переводы с русского на английский
# result = get_translate_ru_to_en(var)

# if not result:
# print("Слово не найдено")
# continue
# else:
# for i, v in enumerate(result):
# print_translate(str(i + 1), v)
# case "a":
# while True:
# var = input()
# if var in ("sr", "s", "u", "d", "q"):
# break
# print("a - пусто")
# case "u":
# while True:
# var = input()
# if var in ("sr", "s", "a", "d", "q"):
# break
# print("u - пусто")
# case "d":
# while True:
# var = input()
# if var in ("sr", "s", "a", "u", "q"):
# break
# print("d - пусто")

# # Выход из программы
# table = Table(title="")
# table.add_column("Выход из программы", justify="center")
# table.add_row("До встречи 🤚")
# Console().print(table)
