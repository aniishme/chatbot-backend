from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from model.models import Query
from model.schemas import QueryCreate

query_router  = APIRouter()


@query_router.post("/")
def create(query: QueryCreate, db: Session = Depends(get_db)):
    db_query = Query(name=query.name, title=query.title, type=query.type, description=query.description)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


@query_router.get("/")
def get_queries(db: Session = Depends(get_db)):
    return db.query(Query).all()