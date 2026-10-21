from db import engine, init_db
from models import Dictionary
from rich.console import Console
from rich.table import Table
from sqlalchemy import select
from sqlalchemy.orm import Session
from time import sleep


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
        return session.scalars(select(Dictionary).where(Dictionary.word == word)).all()


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
                    var = input()
                    if var in ("sr", "a", "u", "d", "q"):
                        break

                    table = Table(title="Пользователи")
                    table.add_column("ID", justify="right")
                    table.add_column("Имя")
                    table.add_column("Email")

                    table.add_row("1", "Андрей", "a@example.com")
                    table.add_row("2", "Иван", "i@example.com")

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
