from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    """Абстрактная модель таблицы с общим конструктором и вспомогательными методами."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def __init__(self, data: dict[str, Any] | None = None, **kwargs: Any) -> None:
        values = {}
        if data:
            values.update(data)
        values.update(kwargs)

        columns = self.__table__.columns.keys()
        for key, value in values.items():
            if key in columns:
                setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def save(self, session) -> "BaseModel":
        session.add(self)
        return self

    def delete(self, session) -> None:
        session.delete(self)

class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    slug: Mapped[str | None] = mapped_column(String(255), unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Brand(BaseModel):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")

class Product(BaseModel):
    __tablename__ = "products"

    dummyjson_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float | None] = mapped_column(Float)
    discount_percentage: Mapped[float | None] = mapped_column(Float)
    rating: Mapped[float | None] = mapped_column(Float)
    stock: Mapped[int | None] = mapped_column(Integer)

    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"))

    category: Mapped[Category | None] = relationship(back_populates="products")
    brand: Mapped[Brand | None] = relationship(back_populates="products")
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

class Review(BaseModel):
    __tablename__ = "reviews"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(Text)
    reviewer_name: Mapped[str | None] = mapped_column(String(255))
    reviewer_email: Mapped[str | None] = mapped_column(String(255))
    date: Mapped[datetime | None] = mapped_column(DateTime)

    product: Mapped[Product] = relationship(back_populates="reviews")



