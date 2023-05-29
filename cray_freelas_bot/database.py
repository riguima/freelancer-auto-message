import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()


db = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Sesssion = sessionmaker(db)
