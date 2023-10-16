from typing import Optional, Union

from sqlmodel import SQLModel, create_engine
from sqlalchemy.future import Engine

from .models import PostgresConn, SqliteConn
from .settings import get_settings


_engine: Optional[Engine] = None


def connect_database():
    global _engine
    if _engine:
        raise Exception("Database engine should be created only once.")

    conn: Union[PostgresConn, SqliteConn]
    settings = get_settings()
    if settings.postgres_url:
        conn = PostgresConn(url=settings.postgres_url)
    else:
        conn = SqliteConn.builder(settings.data_dir, settings.sqlite_filename)

    _engine = create_engine(conn.url)

    SQLModel.metadata.create_all(_engine)
