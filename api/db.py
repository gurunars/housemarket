import os

from contextlib import contextmanager

from functools import lru_cache

from typing import ContextManager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


@lru_cache(1)
def get_sqlite_engine():
    return create_engine(
        "sqlite:///./test.db",
        echo=True,
        connect_args={"check_same_thread": False}
    )


@lru_cache(1)
def get_postgres_engine():
    # "postgresql://user:password@postgresserver/db"
    pass


@lru_cache(1)
def get_engine():
    if "PROD" in os.environ:
        return get_postgres_engine()
    else:
        return get_sqlite_engine()


def get_sqlite_session() -> sessionmaker:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_sqlite_engine()
    )


def get_postgres_session():
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_postgres_engine()
    )


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    if "PROD" in os.environ:
        return get_postgres_session()
    else:
        return get_sqlite_session()


Base = declarative_base()


@contextmanager
def create_session() -> ContextManager[Session]:
    session = get_session_maker()()
    try:
        yield session
    except Exception as exe:
        session.rollback()
        raise exe
    finally:
        session.commit()
        session.close()


def init_db():
    Base.metadata.create_all(bind=get_engine())
