from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserModel(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    campaigns: List[str]

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8)