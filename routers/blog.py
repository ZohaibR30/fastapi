import schemas

from repository import blog
from typing import List
from database import getDb
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix = "/blog",
    tags = ['blogs']
)

@router.get('/', response_model = List[schemas.showBlog])
def all(db: Session = Depends(getDb)):
    return blog.getAll(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(getDb)):
    return blog.create(req, db)

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(getDb)):
    return blog.destroy(id, db)

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id, req: schemas.Blog, db: Session = Depends(getDb)):
    return blog.update(id, req, db)

@router.get('/{id}', status_code = 200, response_model = schemas.showBlog)
def show(id, db: Session = Depends(getDb)):
    return  blog.show(id, db)
