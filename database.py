from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
# Format: mysql+pymysql://username:password@host:port/database_name
# Get from environment variables with fallback to defaults for local development
# Note: These defaults match docker-compose.yml defaults for consistency
DB_USER = os.getenv("DB_USER", "expense_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "expense_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "expense_tracker")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with connection pooling
# Add connect_args to handle connection retries and timeouts
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_timeout=20,     # Wait up to 20 seconds for a connection from the pool
    max_overflow=10,     # Allow up to 10 connections beyond pool_size
    echo=False,          # Set to True for SQL query logging
    connect_args={
        "connect_timeout": 10,  # Connection timeout in seconds
        "read_timeout": 10,     # Read timeout in seconds
        "write_timeout": 10,    # Write timeout in seconds
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency function to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()