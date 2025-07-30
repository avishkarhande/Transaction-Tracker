from sqlalchemy import Column, Date, DateTime, Integer, String

from .database import Base


class PolledData(Base):
    __tablename__ = "polled_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    email = Column(String, index=True)
    name = Column(String)
    subject = Column(String)
    body = Column(String)
    status = Column(String)
    amount = Column(String)
    date = Column(Date)
    vpa = Column(String)
