import readline  # noqa: F401
import subprocess

from db import engine, init_db
from models import Context, Dictionary
from rich.console import Console
from rich.table import Table
from sqlalchemy import Row, String, func, inspect, select  # noqa: F401
from sqlalchemy.orm import Session


def copy_to_clipboard(text: str) -> None:
    """Копировать текст в глобальный буфер"""
    subprocess.run(["clip.exe"], input=text.encode("utf-16"), check=True)


def menu():
    print("\n=======Переводчик (en-ru)=======")
    print("================================")
    print("""Переключение режимов работы:
    s - выполнить перевод c английского на русский
    sr - выполнить перевод c русского на английский
    sc - показать один или несколько контекстов по ключевому слову
    ci - показать контекст по его ID
    a - добавить новый перевод
    ac - добавить новый контекст
    u - редактировать перевод
    uc - редактировать контекст
    d - удалить перевод
    dc - удалить контекст
    m - показать горячие клавиши
    q - выход из программы""")


def add_translate(**kwargs) -> None:
    """Добавить перeвод в базу данных"""
    kwargs2 = {k: v for k, v in kwargs.items() if v}
    with Session(engine) as session:
        session.add(Dictionary(**kwargs2))
        session.commit()


def add_context(context_en, context_ru) -> None:
    """Добавить контекст в базу данных"""
    with Session(engine) as session:
        session.add(Context(context_en=context_en, context_ru=context_ru))
        session.commit()

def update_translate(d: Dictionary, **kwargs) -> None:
    """Редактировать перeвод"""
    kwargs2 = {k: v for k, v in kwargs.items() if v}
    with Session(engine) as session:
        for k, v in kwargs2:
            setattr(d, k, v)
        session.commit()

def get_translate_en_to_ru(_word: str):
    """Получить перевод с английского на русский"""
    with Session(engine) as session:
        stmt = (
            select(
                Dictionary.id,
                Dictionary.word,
                Dictionary.value,
                Dictionary.context_id,
                Context.context_en,
                Context.context_ru,
                Dictionary.comment,
            )
            .outerjoin(Context, Dictionary.context)
            .where(Dictionary.word.ilike(f"%{_word}%"))
        )
        return session.execute(stmt).all()


def get_translate_ru_to_en(_word: str):
    """Получить перевод c русского на английский"""
    with Session(engine) as session:
        stmt = (
            select(
                Dictionary.id,
                Dictionary.word,
                Dictionary.value,
                Dictionary.context_id,
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


def get_dictionary_id(_id: int):
    """Получить контекст по его ID"""
    with Session(engine) as session:
        return session.get(Dictionary, _id)


def get_context_id(_id: int):
    """Получить контекст по его ID"""
    with Session(engine) as session:
        return session.get(Context, _id)


def counter_ref(_id: int) -> int:
    """Сколько записей в translations ссылаются на контекст с данным id"""
    with Session(engine) as session:
        stmt = (
            select(func.count())
            .select_from(Dictionary)
            .where(Dictionary.context_id == _id)
        )
        return session.scalar(stmt) or 0


def max_id(model: type[Dictionary] | type[Context]) -> int:
    """Вернуть максимальный id для таблицы"""
    with Session(engine) as session:
        stmt = select(func.max(model.id))
        return session.scalar(stmt) or 0


def print_translate(title: str, v: Row) -> None:
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
        table.add_row(f"Context (ID: {v.context_id})", style=H3)
        table.add_row(v.context_en)
    if v.context_ru:
        table.add_row("Контекст", style=H4)
        table.add_row(v.context_ru)
    if v.comment:
        table.add_row("Комментарий", style=H5)
        table.add_row(v.comment)
    print()
    Console().print(table)


def print_context(v: Context, title: str | None = None) -> None:
    """Напечатать контекст"""

    H = "bold white on blue"
    H1 = "bold white on yellow"
    H2 = "bold white on magenta"
    H3 = "bold white on green"

    table = Table(title=title, show_lines=True, header_style=H)
    table.add_column("ID", justify="center")
    table.add_row(str(v.id))
    table.add_row("Context: en", style=H1)
    table.add_row(v.context_en)
    table.add_row("Context: ru", style=H2)
    table.add_row(v.context_ru)
    table.add_row("Количество ссылок на данный контекст", style=H3)
    table.add_row(str(counter_ref(int(v.id))))
    print()
    Console().print(table)


def del_context(_id: int):
    """Удалить контекст по его ID"""
    with Session(engine) as session:
        context = session.get(Context, _id)
        if not context:
            print("Контекст с таким ID не существует")
        else:
            print_context(context)
            if (
                input('Подтвердите удаление контекста - введите "yes": ').strip()
                == "yes"
            ):
                session.delete(context)
                session.commit()


def update_context(_id: int):
    """Редактировать контекст"""
    with Session(engine) as session:
        context = session.get(Context, _id)
        if not context:
            print("Контекст с таким ID не существует")
        else:
            print_context(context)

            # Редактирую Context: en
            old_value = context.context_en
            copy_to_clipboard(old_value)
            print('"Context: en"\nСтарое значение для поля находится в буфере обмена.')
            print("Если просто нажать Enter, значение поля не изменится ✅")
            new_val = input("Вы можете вставить его и потом отредактировать:\n").strip()
            if new_val and (old_value != new_val):
                context.context_en = new_val

            # Редактирую Context: ru
            old_value = context.context_ru
            copy_to_clipboard(old_value)
            print("================================")
            print('"Context: ru"\nСтарое значение для поля находится в буфере обмена.')
            print("Если просто нажать Enter, значение поля не изменится ✅")
            new_val = input("Вы можете вставить его и потом отредактировать:\n").strip()
            if new_val and (old_value != new_val):
                context.context_ru = new_val

            session.commit()


if __name__ == "__main__":
    init_db()  # создать таблицы

    # Справка по горячим клавишам
    menu()

    var = "s"
    while var != "q":
        match var:
            case "s":
                while True:
                    print("================================")
                    print("Перевод с английского на русский")
                    print(f"Всего переводов в базе данных: {max_id(Dictionary)}")
                    var = input("Введите слово: ").strip()
                    if var in (
                        "sr",
                        "a",
                        "u",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
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
                    print(f"Всего переводов в базе данных: {max_id(Dictionary)}")
                    var = input("Введите слово: ").strip()
                    if var in (
                        "s",
                        "a",
                        "u",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
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
                    print(f"Максимальный ID: {max_id(Context)}")
                    var = input("Введите слово: ").strip()
                    if var in (
                        "s",
                        "a",
                        "u",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sr",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break

                    # Получить контексты
                    result = get_context(var)

                    if not result:
                        print("Слово не найдено")
                        continue
                    else:
                        for i, v in enumerate(result):
                            print_context(v, str(i + 1))
            case "ci":
                while True:
                    print("================================")
                    print("Получить контекст по его ID")
                    print(f"Максимальный ID: {max_id(Context)}")
                    var = input("Введите ID контекста: ").strip()
                    if var in (
                        "s",
                        "a",
                        "u",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sr",
                        "dc",
                        "m",
                        "sc",
                    ):
                        break

                    # Получить контекст
                    result = get_context_id(int(var))

                    if not result:
                        print("Контекст с таким ID не существует")
                        continue
                    else:
                        print_context(result)
            case "a":
                while True:
                    print("================================")
                    print("Добавить перевод")
                    var = input("Введите слово: ").strip()
                    if var in (
                        "sr",
                        "s",
                        "u",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break
                    value = input("Введите перевод: ").strip().lower()
                    context = input("Введите ID контекста: ")
                    context = int(context) if context.isdigit() else None
                    comment = input("Введите комментарий: ").strip().lower()
                    add_translate(
                        word=var.lower(), value=value, context=context, comment=comment
                    )
            case "ac":
                while True:
                    print("================================")
                    print("Добавить контекст")
                    var = input("Введите контекст: ").strip()
                    if var in (
                        "sr",
                        "s",
                        "u",
                        "d",
                        "q",
                        "a",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break
                    value = input("Введите перевод контекста: ").strip()
                    if var and value:
                        add_context(context_en=var, context_ru=value)
            case "u":
                while True:
                    print("================================")
                    print("Редактировать перевод")
                    var = input("Введите ID перевода: ").strip()
                    if var in (
                        "sr",
                        "s",
                        "a",
                        "d",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break
                    if var.isdigit():
                        # Получаю объект-строку по ее id
                        d = get_dictionary_id(int(var))
                        if d:
                            word =  input("Введите слово (en): ").strip().lower()
                            value = input("Введите перевод (ru): ").strip().lower()
                            comment = input("Введите комментарий: ").strip().lower()
                        else:
                            print("Перевода с таким ID не существует!!!")
                    else:
                        print("Ошибка: вы ввели не число!!!")

                    # add_translate(
                    #     word=var, value=value, context=context, comment=comment
                    # )
            case "uc":
                while True:
                    print("================================")
                    print("Редактировать контекст")
                    var = input("Введите ID контекста: ").strip()
                    if var in (
                        "sr",
                        "s",
                        "a",
                        "d",
                        "q",
                        "ac",
                        "u",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break
                    update_context(int(var))

            case "d":
                while True:
                    var = input()
                    if var in (
                        "sr",
                        "s",
                        "a",
                        "u",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "dc",
                        "m",
                        "ci",
                    ):
                        break
                    print("d - пусто")
            case "dc":
                while True:
                    print("================================")
                    print("Удалить контекст")
                    var = input("Введите ID удаляемой строки контекста: ")
                    if var in (
                        "sr",
                        "s",
                        "a",
                        "u",
                        "q",
                        "ac",
                        "uc",
                        "sc",
                        "d",
                        "m",
                        "ci",
                    ):
                        break
                    del_context(int(var))
            case "m":
                menu()
                var = "s"
            case _:
                print("Недопустимое состояние: выход")
                break

    # Выход из программы
    table = Table(title="")
    table.add_column("Выход из программы", justify="center")
    table.add_row("До встречи 🤚")
    Console().print(table)
