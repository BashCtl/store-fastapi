from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.configs import settings

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASS}"
                           f"@{settings.DB_URI}:{settings.DB_PORT}/{settings.DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
