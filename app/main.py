from db import engine, init_db
from models.dictionary import Dictionary
from sqlalchemy import select
from sqlalchemy.orm import Session


class Translate:

    def add_translate(self, word: str, value: str):
        with Session(engine) as session:
            session.add(Dictionary(word=word, value=value))
            session.commit()

    def add_translate_dict(self, translates: dict):
        with Session(engine) as session:
            dict_list = [Dictionary(word=w, value=v) for w, v in translates.items()]
            session.add_all(dict_list)
            session.commit()

    def get_translate(self, word: str):
        with Session(engine) as session:
            return session.scalars(select(Dictionary).where(Dictionary.word == word)).all()


if __name__ == "__main__":
    init_db()

    for translate in Translate().get_translate("Hello"):
        print(translate)
