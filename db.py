from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

class DatabaseConnection:
    """Класс для подключения к SQLite и PostgreSQL."""

    def __init__(
        self,
        dialect: str = "sqlite",
        database: str = "dummyjson.sqlite3",
        username: str | None = None,
        password: str | None = None,
        host: str = "localhost",
        port: int | None = None,
        driver: str | None = None,
        echo: bool = False,
    ) -> None:
        self.dialect = dialect
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.driver = driver
        self.echo = echo

        self.engine = create_engine(self.url, echo=self.echo)
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def url(self) -> str:
        if self.dialect == "sqlite":
            return f"sqlite:///{Path(self.database).as_posix()}"

        dialect = self.dialect
        if self.driver:
            dialect = f"{dialect}+{self.driver}"

        auth = ""
        if self.username:
            auth = quote_plus(self.username)
            if self.password:
                auth += f":{quote_plus(self.password)}"
            auth += "@"

        port = f":{self.port}" if self.port else ""
        return f"{dialect}://{auth}{self.host}{port}/{self.database}"

    def create_tables(self, base) -> None:
        base.metadata.create_all(self.engine)

    def drop_tables(self, base) -> None:
        base.metadata.drop_all(self.engine)

    def get_session(self) -> Session:
        return self.session_factory()

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_engine(self) -> Engine:
        return self.engine


