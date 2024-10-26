from sqlalchemy import Column, Integer, String , Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

Base = declarative_base()

#validation schema
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(length=100), index=True)
    description = Column(String(length=255), index=True)
    status = Column(Boolean)

class ItemCreate(BaseModel):
    task: str
    description: str
    status : bool

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True  
