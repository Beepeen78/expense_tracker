from sqlalchemy import Column,String,DATE, Integer, ForeignKey, Numeric, DateTime, Text
from database import Base

class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(255))
    expense_date = Column(DATE, nullable=False)
    location = Column(String(255))
    # other fields as needed

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)  # Store hash, not raw password
    
class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)    