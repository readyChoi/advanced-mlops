import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

feature_store_url = os.getenv("FEATURE_STORE_URL")

engine = create_engine(feature_store_url, echo=False)
# 세션을 생성해주는 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 비동기일 경우
# from sqlalchemy.ext.asyncio import create_async_engine
# async_engine = create_async_engine(feature_store_url, echo=False)
# AsyncSessionlocal = async_sessionmaker(autocommit=False)
Base = declarative_base()


def get_db():
    """데이터베이스 세션을 제공하는 함수 (의존성 주입용)"""
    with SessionLocal() as session:
        yield session
