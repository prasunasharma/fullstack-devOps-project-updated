from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time

DATABASE_URL = "postgresql://postgres:postgres@db:5432/app"

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Now initialize SQLAlchemy engine & create tables
MAX_RETRIES = 10
RETRY_DELAY = 3

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Connected to DB and created tables.")
        break
    except OperationalError:
        print(f"❌ Attempt {attempt+1}: Database not ready. Retrying in {RETRY_DELAY}s...")
        time.sleep(RETRY_DELAY)
else:
    raise Exception("⛔ Could not connect to DB after multiple retries.")

# Pydantic schema
class ItemSchema(BaseModel):
    name: str
    description: str

class ItemOut(ItemSchema):
    id: int

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

@app.post("/items", response_model=ItemOut)
def create_item(item: ItemSchema):
    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get("/items", response_model=List[ItemOut])
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemSchema):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    db.close()
