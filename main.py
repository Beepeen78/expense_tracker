from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
import os
import models
import schemas
from database import engine, get_db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here_change_in_production")
if SECRET_KEY == "your_secret_key_here_change_in_production":
    import warnings
    warnings.warn("Using default SECRET_KEY. Please set SECRET_KEY environment variable in production!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize FastAPI app
app = FastAPI(title="Expense Tracker API", version="1.0.0")

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password[:72], hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password[:72])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Expense Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Authentication endpoints
@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# User endpoints
@app.post("/users/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of users (admin only - consider adding admin check)."""
    return db.query(models.User).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int, 
    user: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a user (users can only update themselves)."""
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Users can only update themselves
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a user (users can only delete themselves)."""
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Users can only delete themselves
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_user)
    db.commit()
    return None


# Category endpoints
@app.post("/categories/", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=list[schemas.CategoryOut])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of categories."""
    return db.query(models.Category).offset(skip).limit(limit).all()


@app.get("/categories/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Update a category."""
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if new name already exists
    existing = db.query(models.Category).filter(
        models.Category.name == category.name,
        models.Category.category_id != category_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""
    db_category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category is used by any expenses
    expenses_count = db.query(models.Expense).filter(models.Expense.category_id == category_id).count()
    if expenses_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category: {expenses_count} expense(s) are using this category"
        )
    
    db.delete(db_category)
    db.commit()
    return None


# Expense endpoints
@app.post("/expenses/", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new expense."""
    # Verify category exists
    category = db.query(models.Category).filter(models.Category.category_id == expense.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create expense with current user's ID
    expense_data = expense.dict()
    expense_data["user_id"] = current_user.user_id
    
    db_expense = models.Expense(**expense_data)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses/", response_model=list[schemas.ExpenseOut])
def read_expenses(
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get list of expenses. Users can only see their own expenses."""
    query = db.query(models.Expense).filter(models.Expense.user_id == current_user.user_id)
    
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def read_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific expense by ID. Users can only access their own expenses."""
    expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Users can only access their own expenses
    if expense.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return expense


@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(
    expense_id: int, 
    expense: schemas.ExpenseUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update an expense. Users can only update their own expenses."""
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Users can only update their own expenses
    if db_expense.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Verify category if provided
    if expense.category_id:
        category = db.query(models.Category).filter(models.Category.category_id == expense.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = expense.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete an expense. Users can only delete their own expenses."""
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Users can only delete their own expenses
    if db_expense.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_expense)
    db.commit()
    return None
