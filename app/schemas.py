from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PolledDataCreate(BaseModel):
    timestamp: Optional[datetime]
    email: str
    name: str
    subject: str
    body: str
    status: str
    amount: Optional[str]
    date: Optional[date]
    vpa: Optional[str]


class PolledData(BaseModel):
    id: int
    timestamp: Optional[datetime]
    email: str
    name: str
    subject: str
    body: str
    status: str
    amount: Optional[str]
    date: Optional[date]
    vpa: Optional[str]

    class Config:
        orm_mode = True
