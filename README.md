# 💰 Expense Tracker API

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**A production-ready RESTful API for personal expense management with JWT authentication, user authorization, and automated database migrations.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Deployment](#-deployment) • [Project Analysis](#-project-analysis)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Project Analysis](#-project-analysis)
  - [Strengths](#-strengths)
  - [Known Limitations](#-known-limitations)
  - [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The Expense Tracker API is a comprehensive backend solution for managing personal finances. Built with modern Python frameworks and best practices, it provides secure user authentication, expense tracking, and category management through a well-documented REST API.

### Key Highlights

- 🔐 **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- 🛡️ **Authorization**: Users can only access their own data
- 📊 **Data Validation**: Comprehensive input validation using Pydantic v2
- 🗄️ **Database Migrations**: Automated schema management with Alembic
- 🐳 **Containerized**: Docker and Docker Compose for easy deployment
- 📚 **Auto-Documentation**: Interactive API docs with Swagger UI and ReDoc
- ⚡ **High Performance**: Built on FastAPI for async support and high throughput

---

## ✨ Features

### Authentication & Security
- ✅ JWT-based authentication with configurable token expiration
- ✅ Secure password hashing using bcrypt
- ✅ OAuth2 password flow implementation
- ✅ User-specific data isolation

### User Management
- ✅ User registration with email and username validation
- ✅ User profile management (read, update, delete)
- ✅ Self-service account management

### Expense Management
- ✅ Create, read, update, and delete expenses
- ✅ Category-based expense organization
- ✅ Date-based expense tracking
- ✅ Location and description fields
- ✅ Decimal precision for currency amounts

### Category Management
- ✅ Create and manage expense categories
- ✅ Referential integrity (prevents deletion of categories in use)
- ✅ Unique category names

### Developer Experience
- ✅ Interactive API documentation (Swagger UI)
- ✅ Alternative documentation (ReDoc)
- ✅ Environment-based configuration
- ✅ Comprehensive error handling
- ✅ Type hints throughout the codebase

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** (0.121.2) - Modern, fast web framework for building APIs with automatic OpenAPI documentation

### Database & ORM
- **SQLAlchemy** (2.0.44) - SQL toolkit and ORM with connection pooling
- **MySQL** (8.0) - Relational database for data persistence
- **PyMySQL** (1.1.2) - Pure Python MySQL client
- **Alembic** (1.17.2) - Database migration tool

### Authentication & Security
- **python-jose** (3.5.0) - JWT token handling
- **passlib** (1.7.4) - Password hashing with bcrypt
- **bcrypt** - Secure password hashing algorithm

### Data Validation
- **Pydantic** (2.12.4) - Data validation using Python type annotations
- **Email validation** - Built-in email format validation

### Deployment & DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Uvicorn** - ASGI server for production deployment

### Development Tools
- **python-dotenv** - Environment variable management
- **python-multipart** - Form data handling

---

## 🏗️ Architecture

### System Design

```
┌─────────────────┐
│   Client App    │
│  (Frontend/API) │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
│                 │
│  • Authentication│
│  • Authorization │
│  • Business Logic│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ SQLAlchemy ORM │
│  (models.py)   │
└────────┬───────┘
         │
         ▼
┌─────────────────┐
│   MySQL 8.0     │
│   Database      │
└─────────────────┘
```

### Database Schema

```
users
├── user_id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
└── password_hash

categories
├── category_id (PK)
└── name (UNIQUE)

expenses
├── expense_id (PK)
├── user_id (FK → users.user_id)
├── category_id (FK → categories.category_id)
├── amount (DECIMAL 10,2)
├── description
├── expense_date
├── location
└── created_at
```

### Security Model

- **Authentication**: JWT tokens with configurable expiration
- **Authorization**: User-based data isolation at the application level
- **Password Security**: bcrypt hashing with automatic salt generation
- **Input Validation**: Pydantic schemas validate all user inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (recommended)
- MySQL 5.7+ or MySQL 8.0+ (if not using Docker)

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Beepeen78/expense_tracker.git
cd expense_tracker

# Create environment file
cp .env.example .env
# Edit .env and set your SECRET_KEY

# Start services
docker-compose up -d

# Access the API
# http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

For detailed setup instructions, see [QUICK_START.md](./QUICK_START.md)

---

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication
- `POST /login/` - Authenticate and receive JWT token

#### Users
- `POST /users/` - Create a new user
- `GET /users/me` - Get current user information (authenticated)
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user (self only)
- `DELETE /users/{user_id}` - Delete user (self only)

#### Categories
- `POST /categories/` - Create a category
- `GET /categories/` - List all categories
- `GET /categories/{category_id}` - Get category by ID
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category (if not in use)

#### Expenses
- `POST /expenses/` - Create expense (authenticated)
- `GET /expenses/` - List user's expenses (authenticated)
- `GET /expenses/{expense_id}` - Get expense by ID (authenticated, own only)
- `PUT /expenses/{expense_id}` - Update expense (authenticated, own only)
- `DELETE /expenses/{expense_id}` - Delete expense (authenticated, own only)

### Example Usage

```bash
# 1. Create a user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'

# 2. Login
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"

# 3. Create expense (with token)
curl -X POST "http://localhost:8000/expenses/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "category_id": 1,
    "amount": 25.50,
    "expense_date": "2024-01-15",
    "description": "Lunch at restaurant",
    "location": "Downtown"
  }'
```

---

## 📁 Project Structure

```
expense_tracker/
├── alembic/                 # Database migration scripts
│   ├── versions/            # Migration history
│   └── env.py              # Alembic environment configuration
├── main.py                  # FastAPI application and endpoints
├── models.py                # SQLAlchemy database models
├── schemas.py               # Pydantic validation schemas
├── database.py              # Database connection and session management
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container orchestration
├── Procfile                 # Heroku deployment configuration
├── alembic.ini              # Alembic configuration
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── DEPLOYMENT.md           # Comprehensive deployment guide
├── QUICK_START.md          # Quick start guide
└── README.md               # This file
```

---

## 🚢 Deployment

This project is designed for easy deployment across multiple platforms. See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

### Supported Platforms

- ✅ **Railway** - One-click deployment with automatic MySQL
- ✅ **Render** - Free tier available
- ✅ **Heroku** - Classic PaaS platform
- ✅ **AWS (EC2 + RDS)** - Full control, scalable
- ✅ **DigitalOcean** - Simple and affordable
- ✅ **Fly.io** - Global edge deployment
- ✅ **Docker** - Containerized deployment

### Quick Deploy Commands

```bash
# Docker Compose
docker-compose up -d

# Local development
uvicorn main:app --reload
```

---

## 📊 Project Analysis

### 💪 Strengths

#### 1. **Modern Technology Stack**
- Built with **FastAPI**, one of the fastest Python web frameworks
- Uses **SQLAlchemy 2.0** with modern async capabilities
- **Pydantic v2** for robust data validation
- Follows current Python best practices

#### 2. **Security Best Practices**
- ✅ JWT-based authentication with secure token handling
- ✅ bcrypt password hashing (industry standard)
- ✅ Environment variable configuration for secrets
- ✅ Input validation on all endpoints
- ✅ SQL injection protection via ORM
- ✅ User-level data isolation

#### 3. **Production-Ready Features**
- ✅ Database migrations with Alembic
- ✅ Connection pooling for database efficiency
- ✅ Comprehensive error handling
- ✅ Environment-based configuration
- ✅ Docker containerization
- ✅ Health checks and dependency management

#### 4. **Developer Experience**
- ✅ Auto-generated API documentation (Swagger/ReDoc)
- ✅ Type hints throughout codebase
- ✅ Clear project structure
- ✅ Comprehensive deployment documentation
- ✅ Easy local development setup

#### 5. **Code Quality**
- ✅ Separation of concerns (models, schemas, routes)
- ✅ Dependency injection pattern
- ✅ Consistent error handling
- ✅ Well-documented code
- ✅ Follows RESTful API conventions

#### 6. **Scalability Considerations**
- ✅ Connection pooling for database efficiency
- ✅ Stateless API design (JWT tokens)
- ✅ Containerized for horizontal scaling
- ✅ Environment-based configuration for different environments

---

### ⚠️ Known Limitations

#### 1. **Authentication & Authorization**
- ❌ No refresh token mechanism (tokens expire after 30 minutes)
- ❌ No role-based access control (RBAC) - all users have same permissions
- ❌ No password reset functionality
- ❌ No email verification
- ❌ No account lockout after failed login attempts

#### 2. **Security Enhancements Needed**
- ❌ No rate limiting (vulnerable to brute force attacks)
- ❌ No CORS configuration (needs to be added for frontend integration)
- ❌ No request logging/audit trail
- ❌ No HTTPS enforcement (relies on deployment platform)
- ❌ No input sanitization beyond Pydantic validation

#### 3. **Functionality Gaps**
- ❌ No expense filtering/search capabilities (date range, amount range)
- ❌ No expense aggregation/statistics endpoints
- ❌ No data export functionality (CSV, JSON)
- ❌ No bulk operations for expenses
- ❌ No expense attachments/receipts
- ❌ No recurring expense support

#### 4. **Database & Performance**
- ❌ No database indexing strategy beyond primary keys
- ❌ No query optimization for large datasets
- ❌ No caching layer (Redis/Memcached)
- ❌ No database read replicas for scaling
- ❌ No full-text search capabilities

#### 5. **Testing & Quality Assurance**
- ❌ No unit tests
- ❌ No integration tests
- ❌ No API endpoint tests
- ❌ No test coverage metrics
- ❌ No CI/CD pipeline

#### 6. **Monitoring & Observability**
- ❌ No application logging configuration
- ❌ No health check endpoint (`/health`)
- ❌ No metrics collection (Prometheus, Datadog)
- ❌ No error tracking (Sentry)
- ❌ No performance monitoring (APM)

#### 7. **Documentation**
- ❌ No API versioning strategy
- ❌ No changelog
- ❌ Limited inline code documentation
- ❌ No architecture decision records (ADRs)

---

### 🚀 Future Enhancements

#### Phase 1: Security & Authentication (High Priority)
- [ ] **Refresh Token Implementation**
  - Add refresh token endpoint
  - Implement token rotation
  - Store refresh tokens securely

- [ ] **Password Management**
  - Password reset via email
  - Password strength requirements
  - Password history tracking

- [ ] **Enhanced Security**
  - Rate limiting (using slowapi or similar)
  - CORS middleware configuration
  - Request logging and audit trail
  - Account lockout after failed attempts

#### Phase 2: Functionality Expansion (Medium Priority)
- [ ] **Expense Analytics**
  - Spending statistics by category
  - Monthly/yearly expense reports
  - Budget tracking and alerts
  - Expense trends visualization

- [ ] **Advanced Filtering & Search**
  - Date range filtering
  - Amount range filtering
  - Full-text search on descriptions
  - Multi-criteria filtering

- [ ] **Data Management**
  - CSV/JSON export functionality
  - Bulk expense import
  - Data backup and restore
  - Expense attachments/receipts storage

#### Phase 3: User Experience (Medium Priority)
- [ ] **Recurring Expenses**
  - Create recurring expense templates
  - Automatic expense generation
  - Recurrence pattern management

- [ ] **Categories Enhancement**
  - Category hierarchy/subcategories
  - Category icons/colors
  - Default categories for new users

- [ ] **User Preferences**
  - Currency selection
  - Date format preferences
  - Timezone support

#### Phase 4: Performance & Scalability (High Priority)
- [ ] **Caching Layer**
  - Redis integration for session management
  - Cache frequently accessed data
  - Cache invalidation strategy

- [ ] **Database Optimization**
  - Comprehensive indexing strategy
  - Query optimization
  - Database connection pooling tuning
  - Read replicas for scaling

- [ ] **API Performance**
  - Response compression
  - Pagination improvements
  - Field selection (GraphQL-like)
  - API response caching

#### Phase 5: Testing & Quality (High Priority)
- [ ] **Test Suite**
  - Unit tests (pytest)
  - Integration tests
  - API endpoint tests
  - Test coverage > 80%

- [ ] **CI/CD Pipeline**
  - GitHub Actions workflow
  - Automated testing on PR
  - Automated deployment
  - Code quality checks (linting, formatting)

#### Phase 6: Monitoring & Observability (Medium Priority)
- [ ] **Logging**
  - Structured logging (JSON format)
  - Log levels configuration
  - Request/response logging
  - Error logging with stack traces

- [ ] **Monitoring**
  - Health check endpoint (`/health`, `/ready`)
  - Metrics collection (Prometheus)
  - Error tracking (Sentry)
  - Performance monitoring (APM)

- [ ] **Alerting**
  - Error rate alerts
  - Performance degradation alerts
  - Database connection alerts

#### Phase 7: Advanced Features (Low Priority)
- [ ] **Multi-currency Support**
  - Currency conversion
  - Exchange rate management
  - Multi-currency expense tracking

- [ ] **Collaboration Features**
  - Shared expense categories
  - Expense sharing between users
  - Group expense management

- [ ] **Mobile API Enhancements**
  - Push notifications
  - Offline sync capability
  - Mobile-optimized endpoints

- [ ] **Admin Panel**
  - Admin role implementation
  - User management interface
  - System statistics dashboard

#### Phase 8: Architecture Improvements (Low Priority)
- [ ] **API Versioning**
  - Version strategy (URL-based or header-based)
  - Backward compatibility
  - Deprecation policy

- [ ] **Microservices Migration** (if needed)
  - Service separation (auth, expenses, users)
  - API Gateway implementation
  - Service discovery

- [ ] **Event-Driven Architecture**
  - Message queue integration (RabbitMQ/Kafka)
  - Event sourcing for audit trail
  - Async processing for heavy operations

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write docstrings for all functions and classes
- Update documentation for new features
- Add tests for new functionality

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Bipin Pandey**

- Email: bipinpandey24586@gmail.com
- LinkedIn: [linkedin.com/in/bipinpandey](https://www.linkedin.com/in/bipinpandey)
- GitHub: [@Beepeen78](https://github.com/Beepeen78)

---

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- SQLAlchemy community for the powerful ORM
- All contributors and open-source maintainers

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ using FastAPI and Python

</div>
