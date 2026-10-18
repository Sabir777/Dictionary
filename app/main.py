from pathlib import Path

from models.base import Base
from models.dictionary import Dictionary
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class Translate:
    Singleton = None

    def __new__(cls):
        if cls.Singleton is None:
            cls.Singleton = super().__new__(cls)
        return cls.Singleton

    def __init__(self):

        # создаю подключение к базе данных
        db_path = Path(__file__).parent / "db" / "dictionary.db"
        self.engine = create_engine(f"sqlite:///{db_path}")

        # Создаю таблицы
        Base.metadata.create_all(self.engine)

    def add_translate(self, word: str, value: str):
        with Session(self.engine) as session:
            session.add(Dictionary(word=word, value=value))
            session.commit()

    def add_translate_dict(self, translates: dict):
        with Session(self.engine) as session:
            dict_list = [Dictionary(word=w, value=v) for w, v in translates.items()]
            session.add_all(dict_list)
            session.commit()

    def get_translate(self, word: str):
        with Session(self.engine) as session:
            return session.scalars(select(Dictionary).where(Dictionary.word == word)).all()


if __name__ == "__main__":

    for translate in Translate().get_translate("Hello"):
        print(translate)
