import models, schemas
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

def getAll(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(req: schemas.Blog, db: Session):
    newBlog = models.Blog(title = req.title, body = req.body, userid = req.userid)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

def destroy(id, db: Session):
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

def update(id, req: schemas.Blog, db: Session):
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

def show(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'Detail': f"Blog with id {id} is not available."}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"Blog with id {id} is not available."
        )

    return blog