from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Text
from database import Base

class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    amount = Column(Numeric(10,2))
    expense_date = Column(DateTime)
    description = Column(Text)
    location = Column(Text)
