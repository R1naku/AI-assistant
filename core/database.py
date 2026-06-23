# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Настройки подключения к PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ai_assistant")

# Строка подключения
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,       # Проверка соединения перед использованием
    pool_size=10,             # Размер пула соединений
    max_overflow=20,          # Максимальное дополнительное соединений
    echo=False                # True = видеть SQL запросы в консоли (для отладки)
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """Генератор для получения сессии БД (используется в FastAPI)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("db application")
