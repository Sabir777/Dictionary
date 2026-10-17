from pathlib import Path

from models.base import Base
from models.dictionary import Translate
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

if __name__ == "__main__":
    # создаю подключение к базе данных
    db_path = Path(__file__).parent / "db" / "dictionary.db"
    engine = create_engine(f"sqlite:///{db_path}")

    # Создаю таблицы
    Base.metadata.create_all(engine)

    # Заполняю таблицу
    with Session(engine) as session:
        # Вывожу несколько переводов
        session.add_all(
            [
                Translate(word="Hello", value="Привет"),
                Translate(word="Goodbye", value="Пока"),
                Translate(word="Hi", value="Привет"),
                Translate(word="Bye", value="Пока"),
            ]
        )

        session.commit()

    # Читаю все строки таблицы
    with Session(engine) as session:
        translate_list = session.scalars(select(Translate)).all()
        for translate in translate_list:
            print(translate)
