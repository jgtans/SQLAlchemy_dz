from db import DatabaseConnection
from dummyjson_loader import load_dummyjson
from models import Base

def main() -> None:
    db = DatabaseConnection(dialect="sqlite", database="dummyjson.sqlite3")
    db.create_tables(Base)

    with db.session_scope() as session:
        count = load_dummyjson(session)

    print(f"Loaded {count} products from DummyJSON")

if __name__ == "__main__":
    main()



