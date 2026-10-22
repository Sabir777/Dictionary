from db import engine, init_db
from models import Dictionary
from rich.console import Console
from rich.table import Table
from sqlalchemy import select
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


def get_translate(word: str):
    """Получить перевод по слову"""
    with Session(engine) as session:
        return session.scalars(select(Dictionary).where(Dictionary.word.ilike(f'%{word}%'))).all()


if __name__ == "__main__":
    init_db()  # создать таблицы

    """
    Переключение режимов работы

    s - выполнить перевод слова
    sr - выполнить перевод русского слова
    a - добавить новый перевод
    u - редактировать перевод
    d - удалить перевод
    q - выход из программы
    """

    var = "s"
    while var != "q":
        match var:
            case "s":
                while True:
                    var = input("Введите слово: ")
                    if var in ("sr", "a", "u", "d", "q"):
                        break

                    result = get_translate(var)
                    if not result:
                        print("Слово не найдено")
                        continue

                    H = "bold white on blue"
                    H1 = "bold white on yellow"
                    H2 = "bold white on magenta"
                    H3 = "bold white on green"
                    H4 = "bold white on cyan"
                    H5 = "bold white on bright_black"
                    table = Table(show_lines=True, header_style=H)
                    table.add_column("ID", justify="center")
                    for v in result:
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
            case "sr":
                while True:
                    var = input()
                    if var in ("s", "a", "u", "d", "q"):
                        break
                    print("sr - пусто")
            case "a":
                while True:
                    var = input()
                    if var in ("sr", "s", "u", "d", "q"):
                        break
                    print("a - пусто")
            case "u":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "d", "q"):
                        break
                    print("u - пусто")
            case "d":
                while True:
                    var = input()
                    if var in ("sr", "s", "a", "u", "q"):
                        break
                    print("d - пусто")

        # Выход из программы
        table = Table(title="")
        table.add_column("Выход из программы", justify="center")
        table.add_row("До встречи 🤚")
        Console().print(table)
