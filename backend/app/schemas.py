from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from typing import Optional,List,Literal
from datetime import datetime, date


class UserCreate(BaseModel):
    email:EmailStr
    password: str
    name:Optional[str]=None
    age:Optional[int]=None
    gender:Optional[str]=None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
class UserResponse(BaseModel):
    user_id:UUID
    email:EmailStr
    name:Optional[str]=None
    age:Optional[int]=None
    gender:Optional[str]=None
    is_verfied:bool=False

    class Config:
        from_attributes=True

class Message(BaseModel):
    message: str
    sender:Literal["user","model"]
    timestamp:datetime

class ChatSession(BaseModel):
    user_id: UUID
    session_id:UUID
    messages:List[Message]

    class Config:
        arbitrary_types_allowed=True

class UserLogin(BaseModel):
    email: str
    password: str

class JournalEntryCreate(BaseModel):
    title: str
    content: str
    date: date

class JournalEntryPublic(JournalEntryCreate):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]=None