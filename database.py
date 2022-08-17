from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://myusername:mypassword@localhost/myusername")

SessionLocal = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=engine
            )

Base = declarative_base()