from sqlmodel import Session, SQLModel, create_engine

from config import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
from .models import *


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

SQLModel.metadata.create_all(engine)
