# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.llms import  HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from routes.user import user_router
from routes.query import query_router
from model import models
from pydantic import BaseModel
from database import engine

import uvicorn

import os

from middleware.middleware import is_auth

from model.schemas import UserToken


class Query(BaseModel):
    store_name: str
    query: str

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

def get_conversation_chain(vectorstore):
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.5, model_kwargs={"max_length":256})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(query_router, prefix="/query", tags=["query"])



@app.post("/answer/")
async def get_answer(query:Query, user:UserToken = Depends(is_auth)):
     store = "disastermodel"
     if os.path.exists(f"{store}.pkl"):
        with open(f"{store}.pkl", "rb") as f:
            VectorStore = pickle.load(f)

            chain = get_conversation_chain(VectorStore)
        
            response = chain.invoke({'question': query.query})
            
            return {"response": response, "user":user}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)