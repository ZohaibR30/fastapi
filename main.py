from operator import ne
import schemas, models
from typing import List
from sqlalchemy.orm import Session 
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext 

app = FastAPI()

models.Base.metadata.create_all(engine)

def getDb():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code = status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(getDb)):
    newBlog = models.Blog(title = req.title, body = req.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'Detail': f"Blog with id {id} is not available."}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"Blog with id {id} is not available."
        )

    else:   
        db.query(models.Blog).filter(models.Blog.id == id).delete()
        db.commit()
        return JSONResponse(content = {"message": 'Deletion Done'})

@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(id, req: schemas.Blog, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'Detail': f"Blog with id {id} is not available."}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"Blog with id {id} is not available."
        )

    else:   
        db.query(models.Blog).filter(models.Blog.id == id).update({
            "title": req.title,
            "body": req.body
        })
        db.commit()
        return JSONResponse(content = {"message": 'Updation Done'})


@app.get('/blog', response_model = List[schemas.showBlog])
def all(db: Session = Depends(getDb)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code = 200, response_model = schemas.showBlog)
def show(id, res: Response, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'Detail': f"Blog with id {id} is not available."}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"Blog with id {id} is not available."
        )

    return blog

pwd_cxt = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

@app.post('/user')
def createUser(req: schemas.User, db: Session = Depends(getDb)):
    hashedPassword = pwd_cxt.hash(req.password)
    newUser = models.User(name = req.name, email = req.email, password = hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser