from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

import app_logger

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData(engine)
Base = declarative_base()

class SQL():
    def __init__(self):
        self.logger = app_logger.get_logger(__name__)

    def get_hardware(self):
        bottles_table = Table('bottles', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select(bottles_table)
                rs = con.execute(sthm)
                return rs.fetchall()
        except Exception as ex:
            self.logger.error(str(ex))