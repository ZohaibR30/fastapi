from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    userid: int

class User(BaseModel):
    name: str
    email: str
    password: str

class showUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True

class showBlog(BaseModel):
    title: str
    body: str
    creator : showUser

    class Config():
        orm_mode = True

class login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None