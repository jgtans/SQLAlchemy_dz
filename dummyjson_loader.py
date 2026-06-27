import json
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Brand, Category, Product, Review

DUMMYJSON_PRODUCTS_URL = "https://dummyjson.com/products?limit=0"

def fetch_products(url: str = DUMMYJSON_PRODUCTS_URL) -> list[dict[str, Any]]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 SQLAlchemyHomework/1.0",
        },
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("products", [])

def get_or_create(session: Session, model, **values):
    instance = session.scalar(select(model).filter_by(**values))
    if instance:
        return instance

    instance = model(values)
    session.add(instance)
    session.flush()
    return instance

def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).replace(tzinfo=None)

def save_products(session: Session, products_data: list[dict[str, Any]]) -> None:
    for item in products_data:
        category = None
        if item.get("category"):
            category = get_or_create(
                session,
                Category,
                name=item["category"],
                slug=item["category"].lower().replace(" ", "-"),
            )

        brand = None
        if item.get("brand"):
            brand = get_or_create(session, Brand, name=item["brand"])

        product = session.scalar(
            select(Product).where(Product.dummyjson_id == item["id"])
        )
        if product is None:
            product = Product()
            session.add(product)

        product.dummyjson_id = item["id"]
        product.title = item.get("title", "")
        product.description = item.get("description")
        product.price = item.get("price")
        product.discount_percentage = item.get("discountPercentage")
        product.rating = item.get("rating")
        product.stock = item.get("stock")
        product.category = category
        product.brand = brand

        product.reviews.clear()
        for review_data in item.get("reviews", []):
            product.reviews.append(
                Review(
                    {
                        "rating": review_data.get("rating"),
                        "comment": review_data.get("comment"),
                        "reviewer_name": review_data.get("reviewerName"),
                        "reviewer_email": review_data.get("reviewerEmail"),
                        "date": parse_datetime(review_data.get("date")),
                    }
                )
            )

def load_dummyjson(session: Session) -> int:
    products = fetch_products()
    save_products(session, products)
    return len(products)





