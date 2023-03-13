from typing import Optional

from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.ext.declarative import declarative_base

from post import Post

sqlite_url = "sqlite:///database.db"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session