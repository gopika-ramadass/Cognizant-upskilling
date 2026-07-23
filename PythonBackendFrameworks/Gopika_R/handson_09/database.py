import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_FILE = os.path.join(os.path.dirname(__file__), "auth_demo.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a SQLAlchemy database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
