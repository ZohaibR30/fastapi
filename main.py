import schemas, models
from sqlalchemy.orm import Session 
from database import SessionLocal, engine
from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
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


@app.get('/blog')
def all(db: Session = Depends(getDb)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code = 200)
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