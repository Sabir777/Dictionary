from pathlib import Path

from models import Base
from sqlalchemy import create_engine

# создаю подключение к базе данных
db_path = Path(__file__).parent / "dictionary.db"
engine = create_engine(f"sqlite:///{db_path}")


def init_db() -> None:
    # Создаю таблицы
    Base.metadata.create_all(engine)
