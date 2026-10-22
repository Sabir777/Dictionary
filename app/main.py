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

                    table = Table(title=var)
                    table.add_column("№", justify="right")
                    table.add_column("Значение")
                    table.add_column("Context")
                    table.add_column("Контекст")
                    table.add_column("Комментарий")
                    for i, v in enumerate(result):
                        table.add_row(str(i + 1), v.value, v.context_en, v.context_ru, v.comment)
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
