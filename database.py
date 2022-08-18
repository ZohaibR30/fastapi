from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://myusername:mypassword@localhost/myusername", echo=True)

SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=engine
            )

Base = declarative_base()

def getDb():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()