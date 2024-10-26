from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


DATABASE_URL = "mysql+pymysql://root:root@localhost/folder_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
