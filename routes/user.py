from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext


from model.schemas import UserCreate, UserLogin
from model.models import User

user_router  = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user's password
    hash_password = pwd_context.hash(user.password)

    # Create a new user instance and save it to the database
    db_user = User(name=user.name, email=user.email, password=hash_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@user_router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and pwd_context.verify(user.password, db_user.password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")