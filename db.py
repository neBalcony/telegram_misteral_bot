# contextvar для текущей сессии
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)