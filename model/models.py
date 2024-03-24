from database import Base
from sqlalchemy import Table,ForeignKey, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="RES")
    password = Column(String)
    messages = relationship('Message', back_populates='user')


class Query(Base):
    __tablename__= "query"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    title = Column(String, index=True)
    type = Column(String, index=True)
    description = Column(Text, index=True)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    user = relationship('User', back_populates='messages')
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class FileData(Base):
    __tablename__ = 'filedata'
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    path = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))