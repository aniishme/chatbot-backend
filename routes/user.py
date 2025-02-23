from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

from middleware.middleware import is_auth

from model.schemas import UserCreate, UserLogin, UserToken
from model.models import User

from variables import SECRET_KEY, ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

user_router  = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@user_router.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user's password
    hash_password = pwd_context.hash(user.password)

    # Create a new user instance and save it to the database
    db_user = User(name=user.name, email=user.email, password=hash_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@user_router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and pwd_context.verify(user.password, db_user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"id":db_user.id,"email":user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "role":db_user.role}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

@user_router.delete("/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    print("here:",user_id)
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@user_router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@user_router.get('/hello/')
def get_hello(user:UserToken = Depends(is_auth)):
    return user