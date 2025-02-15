from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


SQLITE_DATABASE_URL = "sqlite:///./tasks.db"

sqlite_engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
sqlite_connection = sqlite_engine.connect()
SqliteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_connection)


@contextmanager
def get_db() -> Session:
    db: Session = SqliteSessionLocal()

    try:
        yield db
    finally:
        db.close()
