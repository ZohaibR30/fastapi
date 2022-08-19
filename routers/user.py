import schemas

from repository import user
from database import getDb
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix = "/user",
    tags = ['Users']
)

@router.post('/', response_model = schemas.showUser)
def createUser(req: schemas.User, db: Session = Depends(getDb)):
    return user.createUser(req, db)

@router.get('/{id}', response_model = schemas.showUser)
def getUser(id, db: Session = Depends(getDb)):
    return user.getUser(id, db)