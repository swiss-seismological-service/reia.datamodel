import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import MetaData

from reia.datamodel.base import ORMBase

__import__("pkg_resources").declare_namespace(__name__)

# session = scoped_session(sessionmaker(autocommit=False,
#                                       bind=engine,
#                                       future=True))


# ORMBase.query = session.query_property()

def load_engine():
    load_dotenv(f'{os.getcwd()}/.env')  # load environment variables

    DB_CONNECTION_STRING = \
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:" \
        f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}" \
        f":{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

    engine = create_engine(DB_CONNECTION_STRING, echo=False, future=True)
    return engine


def init_db():
    """
    Initializes the Database.
    All DB modules need to be imported when calling this function.
    """
    engine = load_engine()
    ORMBase.metadata.create_all(engine)


def drop_db():
    """Drops all database Tables but leaves the DB itself in place"""
    engine = load_engine()
    m = MetaData()
    m.reflect(engine)
    m.drop_all(engine)
