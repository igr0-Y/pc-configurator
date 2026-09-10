import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()