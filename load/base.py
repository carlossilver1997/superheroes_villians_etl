import os
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from dotenv import load_dotenv

load_dotenv()


DB_USER_NAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT = (
    os.getenv('DB_USER_NAME'), 
    os.getenv('DB_PASSWORD'), 
    os.getenv('DB_HOST'), 
    os.getenv('DB_NAME'),
    os.getenv('DB_PORT')
)
url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DB_USER_NAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

engine = create_engine(url)
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(bind=engine)


Base = declarative_base()