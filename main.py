from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


SQLALCHEMY_DATABASE_URL = "sqlite:///./test1.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Items(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(50), unique=True)
    quantity = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
from fastapi.staticfiles import StaticFiles
# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity; tighten this for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Pydantic models
class ItemBase(BaseModel):
    #item_name: str
    quantity: int

class ItemCreate(BaseModel):
    item_name: str
    quantity: int

class ItemDisplay(BaseModel):
    item_id: int
    item_name: str
    quantity: int

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})


@app.post("/add_item", response_model=ItemDisplay)
def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Items).filter(Items.item_name == item.item_name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="Item already registered")
    new_item = Items(item_name=item.item_name, quantity=item.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.get("/items", response_model=List[ItemDisplay])
def read_items(db: Session = Depends(get_db)):
    items = db.query(Items).all()
    return items

@app.delete("/delete_item/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Items).filter(Items.item_id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}

@app.put("/update_item/{item_name}", response_model=ItemDisplay)
def update_item(item_name: str, item: ItemBase, db: Session = Depends(get_db)):
    db_item = db.query(Items).filter(Items.item_name == item_name).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    #db_item.item_name = item.item_name
    db_item.quantity = item.quantity
    db.commit()
    db.refresh(db_item)
    return db_item

import uvicorn
if __name__=='__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)    
