# main.py
from fastapi import FastAPI, Depends, UploadFile, File
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from routes.user import user_router
from routes.query import query_router
from model import models
from pydantic import BaseModel
from database import engine

import uvicorn

from middleware.middleware import is_auth

from model.schemas import UserToken

from chatbot import process_dataset, user_input



class Query(BaseModel):
    store_name: str
    query: str

class Chat(BaseModel):
    query:str

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(query_router, prefix="/query", tags=["query"])


@app.post("/upload/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    print(files)
    process_dataset(files)
    return {"message":"Dataset processed successfylly"}


@app.post('/chat')
async def get_chat(query:Chat):
    if query.query:
        response = user_input(query.query)

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)