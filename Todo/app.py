from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from module.models import  Item, ItemCreate, ItemResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from database.db import *

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items", response_model=ItemResponse)
def create_todo(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = Item(task=item.task,description=item.description,status=item.status)  
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException (status_code= 404, detail= ' Database not fund{e}')
    finally:
        db.close()

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_todo(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException( status_code= 404 , detail='Database Not Found{e}')
    finally:
        db.close()

@app.put("/items/{items_id}",response_model=ItemResponse)
async def update_todo(item_id: int, name: str = None, description: str = None, status: bool = None,db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            if name is not None:
                item.task = name
            if description is not None:
                item.description = description
            if status is not None:
                item.status = status
            db.commit()
            print(f"Updated Successfully: {item}")
            return item
        else:
            raise HTTPException(status_code=404, detail='Item not found')
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=404, detail='Error updating item')
    
    finally:
        db.close()
    
@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_todo(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(item)
        db.commit()
        
        return item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=404 , detail='Database not found{e}')
    finally:
        db.close()


@app.get("/todo")
def get(db : Session = Depends(get_db)):
    try:
        todo = db.query(Item).all()
        return todo
    except SQLAlchemyError as e :
        raise HTTPException(status_code=404, detail='Not found') 
    finally:
        db.close()