"""
models.py - Модели базы данных и DTO объекты
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from db import Base


# ==========================================
# МОДЕЛИ ТАБЛИЦ И СВЯЗИ
# ==========================================
class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Связь один-ко-многим: у одного бренда много товаров
    products = relationship('Product', back_populates='brand')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Связь один-ко-многим: в одной категории много товаров
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    # Foreign Keys (Внешние ключи)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    # Настройка связей (Relationships)
    brand = relationship('Brand', back_populates='products')
    category = relationship('Category', back_populates='products')
    reviews = relationship('Review', back_populates='product', cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)

    # Foreign Key
    product_id = Column(Integer, ForeignKey('products.id'))

    # Связь многие-к-одному (обратная к Product)
    product = relationship('Product', back_populates='reviews')


# ==========================================
# PYDANTIC DTO
# ==========================================
class ProductDTO(BaseModel):
    """Data Transfer Object для товара"""
    id: int
    title: str
    description: str
    price: float
    brand_id: int
    category_id: int

    # В Pydantic V2 для работы с ORM используется model_config
    model_config = {
        "from_attributes": True
    }