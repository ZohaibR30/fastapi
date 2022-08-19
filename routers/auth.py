import schemas, database, models, tokengenerator
from sqlalchemy.orm import Session 
from passlib.context import CryptContext 
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    tags = ['Authentication']
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/login')
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDb)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'Detail': f"Blog with id {id} is not available."}

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid Credentials"
        )

    if not pwd_cxt.verify(req.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Incorrect Password"
        )

    access_token = tokengenerator.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}