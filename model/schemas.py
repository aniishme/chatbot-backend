from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role:str

class UserLogin(BaseModel):
    email: str
    password: str

class UserToken(BaseModel):
    id:str
    password:str
    exp:str

class QueryCreate(BaseModel):
    name:str
    title: str
    type: str
    description: str

