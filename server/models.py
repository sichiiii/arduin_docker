from sqlalchemy import Column, Integer
from database import Base


class Bottles(Base):
    __tablename__ = "bottles"

    id = Column(Integer, primary_key=True, index=True)
    flat = Column(Integer)
    count = Column(Integer)
