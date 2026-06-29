"""
main.py - Точка входа в приложение
"""

from db import Session, init_db
from models import Product, ProductDTO
from dummyjson_loader import populate_from_dummyjson


def display_raw_data(session):
    """
    Получает данные из таблицы products и выводит на экран
    session.query()
    """
    print("--- СЫРЫЕ ДАННЫЕ ИЗ ORM ОБЪЕКТОВ ---")

    # Используем session.query() для выборки
    products = session.query(Product).all()

    for p in products:
        # Обращаемся к связям напрямую (благодаря relationship JOIN делать не нужно)
        brand_name = p.brand.name if p.brand else "Нет бренда"
        print(f"[{p.id}] {p.title} | Цена: {p.price} | Бренд: {brand_name}")

    print("-" * 40 + "\n")


def display_dto_data(session):
    """
    Преобразует ORM объекты в DTO и выводит на экран
    model_validate()
    """
    print("--- ДАННЫЕ В ФОРМАТЕ PYDANTIC DTO ---")

    products = session.query(Product).all()

    for p in products:
        # Используем model_validate для преобразования ORM объекта в Pydantic модель
        # (строго по конспекту 24.pdf)
        dto = ProductDTO.model_validate(p, from_attributes=True)

        # Выводим в формате словаря
        print(dto.model_dump())

    print("-" * 40)


def main():
    """Главная функция приложения"""
    # Инициализируем базу данных (создаем таблицы)
    init_db()

    # Создаем сессию для работы с БД
    session = Session()

    try:
        # 1. Заполняем БД данными из DummyJSON
        populate_from_dummyjson(session, limit=5)

        # 2. Выводим обычные ORM объекты
        display_raw_data(session)

        # 3. Выводим через Pydantic DTO
        display_dto_data(session)

    finally:
        # Закрываем сессию
        session.close()


if __name__ == '__main__':
    main()