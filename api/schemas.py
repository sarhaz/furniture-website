from pydantic import BaseModel
from typing import Optional
import os


class RegisterModel(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_staff: bool
    is_active: bool


class LoginModel(BaseModel):
    username: str
    password: str


class BlogModel(BaseModel):
    id: int
    title: str
    author: str
    comments_id: int
    created_at: int


class CartModel(BaseModel):
    id: int
    count: int
    user_id: int
    status: str


class ProductModel(BaseModel):
    id: int
    name: str
    price: float
    user_id: int
    price_type: str
    description: str


class UserOrderModel(BaseModel):
    username: str


class TeamModel(BaseModel):
    id: int
    text: str


class CommentModel(BaseModel):
    id: int
    text: str
