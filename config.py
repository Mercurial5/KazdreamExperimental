from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(getenv('DATABASE_URI'), future=True, pool_pre_ping=True)
Base = declarative_base()
