from sqlalchemy import create_engine
from utils import config


engine = create_engine(config.SA_URL)
