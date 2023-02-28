from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import (DB_ENGINE, DB_HOST, DB_NAME, DB_PORT, POSTGRES_PASSWORD,
                                 POSTGRES_USER)


class Base(DeclarativeBase):
    pass


def get_session(engine):
    session = sessionmaker(bind=engine)
    return session()


engine = create_engine(
    f"{DB_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
