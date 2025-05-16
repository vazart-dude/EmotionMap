from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class Marker(SqlAlchemyBase):
    __tablename__ = 'markers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    emotion = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    username = Column(String, nullable=False) 