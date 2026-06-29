"""
db.py - Настройка подключения к базе данных
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# НАСТРОЙКА И СОЗДАНИЕ БД
engine = create_engine('sqlite:///dummyjson_shop.sqlite3', echo=False)

# Базовый класс для всех моделей
Base = declarative_base()

# Фабрика сессий
Session = sessionmaker(bind=engine)


def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(engine)