# Expense Tracker API

A RESTful API for tracking personal expenses built with FastAPI, SQLAlchemy, and MySQL. This application provides user authentication, expense management, and category organization.

## Features

- **User Authentication**: Secure JWT-based authentication with password hashing
- **User Management**: Create, read, update, and delete user accounts
- **Expense Management**: Full CRUD operations for expenses
- **Category Management**: Organize expenses by categories
- **Authorization**: Users can only access their own expenses
- **Data Validation**: Comprehensive input validation using Pydantic
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Bcrypt**: Password hashing
- **Uvicorn**: ASGI server

## Prerequisites

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)

## Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd expense_tracker
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up MySQL database**:
   - Create a MySQL database named `expense_tracker`:
     ```sql
     CREATE DATABASE expense_tracker;
     ```
   - Update the database connection in `database.py` if needed:
     ```python
     SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/expense_tracker"
     ```

6. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /login/` - Login and get access token
  - Body: `username` and `password` (form data)
  - Returns: `access_token` and `token_type`

### Users

- `POST /users/` - Create a new user
- `GET /users/me` - Get current user information (requires authentication)
- `GET /users/` - Get list of users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user (users can only update themselves)
- `DELETE /users/{user_id}` - Delete user (users can only delete themselves)

### Categories

- `POST /categories/` - Create a new category
- `GET /categories/` - Get list of categories
- `GET /categories/{category_id}` - Get category by ID
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category (only if not used by expenses)

### Expenses

- `POST /expenses/` - Create a new expense (requires authentication)
- `GET /expenses/` - Get list of expenses (users see only their own)
- `GET /expenses/{expense_id}` - Get expense by ID (users can only access their own)
- `PUT /expenses/{expense_id}` - Update expense (users can only update their own)
- `DELETE /expenses/{expense_id}` - Delete expense (users can only delete their own)

## Usage Examples

### 1. Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Category

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Food"
  }'
```

### 4. Create an Expense (with authentication)

```bash
curl -X POST "http://localhost:8000/expenses/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "user_id": 1,
    "category_id": 1,
    "amount": 25.50,
    "expense_date": "2024-01-15",
    "description": "Lunch at restaurant",
    "location": "Downtown"
  }'
```

### 5. Get Expenses (with authentication)

```bash
curl -X GET "http://localhost:8000/expenses/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

### Users Table
- `user_id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`

### Categories Table
- `category_id` (Primary Key)
- `name` (Unique)

### Expenses Table
- `expense_id` (Primary Key)
- `user_id` (Foreign Key → users.user_id)
- `category_id` (Foreign Key → categories.category_id)
- `amount` (Decimal 10,2)
- `description`
- `expense_date`
- `location`
- `created_at`

## Security Notes

⚠️ **Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `main.py` to a strong, random secret
2. Use environment variables for sensitive configuration (database credentials, secret keys)
3. Enable HTTPS
4. Implement rate limiting
5. Add input sanitization
6. Consider adding admin roles for user management
7. Implement proper logging and monitoring

## Project Structure

```
expense_tracker/
├── main.py           # FastAPI application and endpoints
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic schemas for validation
├── database.py       # Database configuration
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

You can test the API using:
- Swagger UI at `/docs`
- Postman
- curl commands
- Any HTTP client

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues and enhancement requests!
