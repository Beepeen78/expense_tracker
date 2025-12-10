from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class UserOut(UserBase):
    user_id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


class UserLogin(BaseModel):
    username: str
    password: str


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    category_id: int
    
    class Config:
        from_attributes = True


# Expense schemas
class ExpenseBase(BaseModel):
    category_id: int
    amount: Decimal = Field(..., gt=0, decimal_places=2)  # Changed to Decimal, must be positive
    expense_date: date  # Changed to date to match model
    description: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)


class ExpenseCreate(ExpenseBase):
    user_id: Optional[int] = None  # Will be set from current_user automatically


class ExpenseUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    expense_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)


class ExpenseOut(ExpenseBase):
    expense_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
