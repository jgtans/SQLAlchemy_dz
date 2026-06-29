"""
dummyjson_loader.py - Загрузка данных из DummyJSON API
"""

import requests
from sqlalchemy.orm import Session
from models import Brand, Category, Product, Review


def get_or_create(session: Session, model, **kwargs):
    """
    Вспомогательная функция: найти объект или создать новый,
    чтобы избежать дублей в базе данных
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def populate_from_dummyjson(session: Session, limit: int = 5):
    """
    Загружает данные из DummyJSON API и сохраняет в базу данных

    Args:
        session: SQLAlchemy сессия
        limit: количество товаров для загрузки (по умолчанию 5)
    """
    print(f"Загрузка {limit} товаров с DummyJSON...")

    # Получаем товары из API
    response = requests.get(f'https://dummyjson.com/products?limit={limit}')
    # Проверка на ошибки HTTP
    response.raise_for_status()
    data = response.json()['products']

    for item in data:
        # В DummyJSON бренд может отсутствовать, подставим 'Unknown'
        brand_name = item.get('brand') or 'Unknown'
        category_name = item.get('category', 'general')

        # Находим или создаем бренд и категорию
        brand = get_or_create(session, Brand, name=brand_name)
        category = get_or_create(session, Category, name=category_name)

        # Создаем товар (используем add)
        product = Product(
            title=item['title'],
            description=item['description'],
            price=item['price'],
            brand_id=brand.id,
            category_id=category.id
        )
        session.add(product)
        session.commit()  # Коммитим, чтобы получить ID товара для отзывов

        # Добавляем отзывы (в DummyJSON они идут внутри объекта товара)
        for rev_data in item.get('reviews', []):
            review = Review(
                rating=rev_data['rating'],
                comment=rev_data['comment'],
                product_id=product.id
            )
            session.add(review)
        session.commit()

    print(f"✅ Успешно загружено {len(data)} товаров!\n")