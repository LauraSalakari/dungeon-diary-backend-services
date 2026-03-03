from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List
from mongodb import user_collection


class UserModel(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    campaigns: List[str]

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8)

class UserCreatedResult(BaseModel):
    id: str
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str


def fetch_user(user_id: str):
    return user_collection.find_one({"_id": ObjectId(user_id)})