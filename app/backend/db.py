from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:////Users/nataliya/Library/Mobile Documents/com~apple~CloudDocs/Python projects/Project FastAPI/app/taskmanager.db',
                       echo = True)

SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase):
    pass
