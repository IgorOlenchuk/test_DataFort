import logging

from sqlalchemy.engine import url as sa_url
from sqlalchemy_utils import database_exists, create_database

from utils import config


if __name__ == "__main__":
    SA_URL = sa_url.make_url(config.ALEMBIC_SA_URL)

    if not database_exists(SA_URL):
        create_database(SA_URL)
        logging.info("database created")
    else:
        logging.info("database already exists")
