from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    user_id: int
    category_id: int
    amount: float
    expense_date: datetime
    description: str = None
    location: str = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    expense_id: int
    class Config:
        orm_mode = True
