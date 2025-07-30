from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import database, models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/push")
def push_data(data: schemas.PolledDataCreate, db: Session = Depends(get_db)):
    db_data = models.PolledData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"id": db_data.id, "message": "Data stored"}


@app.post("/get_all_records", response_model=List[schemas.PolledData])
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(models.PolledData).all()
    return records
