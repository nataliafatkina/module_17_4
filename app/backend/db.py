from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:////Users/nataliya/Library/Mobile Documents/com~apple~CloudDocs/Python projects/HomeWorks_Urban/Module_17/app/taskmanager.db',
                       echo = True)

SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase):
    pass
