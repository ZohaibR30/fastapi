import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from passlib.context import CryptContext 

pwd_cxt = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def createUser(req: schemas.User, db: Session):
    hashedPassword = pwd_cxt.hash(req.password)
    newUser = models.User(name = req.name, email = req.email, password = hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

def getUser(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"Blog with id {id} is not available."
        )
    
    else:
        return user