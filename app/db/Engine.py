from pathlib import Path

from models.base import Base
from sqlalchemy import create_engine

# создаю подключение к базе данных
db_path = Path(__file__).parent / "db" / "dictionary.db"
engine = create_engine(f"sqlite:///{db_path}")

# Создаю таблицы
Base.metadata.create_all(engine)
