from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from excel import Excel
from sqlalchemy import *

from main import SerialPortConnection

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
        self.excel = Excel()
        self.logger = app_logger.get_logger(__name__)


    def add_bottle(self, flat, house_number):
        bottles_table = Table('bottles', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select([bottles_table.c.count]).where(bottles_table.c.flat == flat)
                count = con.execute(sthm).fetchall()

                if count != []:
                    bottle_count = count[0][0]
                    sthm = update(bottles_table).where(and_(bottles_table.c.flat == flat, bottles_table.c.house_number == house_number)).values(count=bottle_count+1)
                    con.execute(sthm)
                else:
                    sthm = insert(bottles_table).values(flat=flat, count=1, house_number=house_number)
                    con.execute(sthm)
            return
        except Exception as ex:
            self.logger.error(str(ex))

    def get_flats(self):
        bottle_table = Table('bottles', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select([bottle_table.c.flat])
                flats = [item[0] for item in con.execute(sthm).fetchall()]
                return flats
        except Exception as ex:
            self.logger.error(str(ex))

    def update_flats(self, start, end, house_number):
        bottle_table = Table('bottles', meta, autoload=True)
        try:
            with engine.connect() as con:
                for flat in range(start, end):
                    sthm = select([bottle_table.c.id]).where(and_(bottle_table.c.flat == flat, bottle_table.c.house_number == house_number))
                    exists = con.execute(sthm).fetchall()
                    if not exists:
                        sthm = insert(bottle_table).values(flat=flat, count=0, house_number=house_number)
                        con.execute(sthm)
            return
        except Exception as ex:
            self.logger.error(str(ex))

    def export(self):
        bottle_table = Table('bottles', meta, autoload=True)
        try:
            with engine.connect() as con:
                sthm = select([bottle_table.c.flat, bottle_table.c.count, bottle_table.c.house_number])
                query = con.execute(sthm).fetchall()
                self.excel.export_to_excel(query)
            return 'ok'
        except Exception as ex:
            self.logger.error(str(ex))
