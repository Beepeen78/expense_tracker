# Deployment Guide for Expense Tracker API

This guide covers multiple deployment options for the Expense Tracker API.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [Local Development with Docker](#local-development-with-docker)
4. [Deployment Options](#deployment-options)
   - [Railway](#railway)
   - [Render](#render)
   - [Heroku](#heroku)
   - [AWS (EC2 + RDS)](#aws-ec2--rds)
   - [DigitalOcean](#digitalocean)
   - [Fly.io](#flyio)
5. [Post-Deployment](#post-deployment)

---

## Prerequisites

- Python 3.8+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- MySQL 5.7+ or MySQL 8.0+ (for local database)
- Git

---

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Required environment variables:

```env
# Database Configuration
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=3306
DB_NAME=expense_tracker

# Security (IMPORTANT: Change in production!)
SECRET_KEY=your_very_long_and_random_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Local Development with Docker

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Beepeen78/expense_tracker.git
   cd expense_tracker
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

3. **Start services with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

5. **View logs:**
   ```bash
   docker-compose logs -f api
   ```

6. **Stop services:**
   ```bash
   docker-compose down
   ```

### Manual Setup (Without Docker)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database:**
   ```sql
   CREATE DATABASE expense_tracker;
   CREATE USER 'expense_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON expense_tracker.* TO 'expense_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Deployment Options

### Railway

[Railway](https://railway.app) is a modern platform that makes deployment easy.

#### Steps:

1. **Sign up at [railway.app](https://railway.app)**

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account and select the repository

3. **Add MySQL Database:**
   - Click "New" → "Database" → "MySQL"
   - Railway will automatically create a MySQL instance

4. **Configure Environment Variables:**
   - Go to your service → "Variables"
   - Add the following variables:
     ```
     DB_USER=<from MySQL service>
     DB_PASSWORD=<from MySQL service>
     DB_HOST=<from MySQL service>
     DB_NAME=<from MySQL service>
     DB_PORT=3306
     SECRET_KEY=<generate a secure key>
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```
   - Railway provides these values in the MySQL service's "Variables" tab

5. **Deploy:**
   - Railway will automatically detect the Dockerfile and deploy
   - Or configure the build command: `pip install -r requirements.txt`
   - Start command: `alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT`

6. **Access your API:**
   - Railway provides a public URL (e.g., `https://your-app.railway.app`)

---

### Render

[Render](https://render.com) offers free tier hosting with automatic deployments.

#### Steps:

1. **Sign up at [render.com](https://render.com)**

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select "Web Service"

3. **Configure Build Settings:**
   - **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add MySQL Database:**
   - Create a new "PostgreSQL" or use "MySQL" (if available)
   - Note: Render's free tier uses PostgreSQL, but you can use a managed MySQL service

5. **Set Environment Variables:**
   ```
   DB_USER=<database_user>
   DB_PASSWORD=<database_password>
   DB_HOST=<database_host>
   DB_PORT=3306
   DB_NAME=<database_name>
   SECRET_KEY=<generate_secure_key>
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Deploy:**
   - Render will automatically deploy on every push to main branch

---

### Heroku

[Heroku](https://www.heroku.com) is a popular PaaS platform.

#### Steps:

1. **Install Heroku CLI:**
   ```bash
   # Visit https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku App:**
   ```bash
   heroku create your-app-name
   ```

4. **Add MySQL Add-on:**
   ```bash
   heroku addons:create cleardb:ignite  # Free tier MySQL
   # Or use JawsDB MySQL
   heroku addons:create jawsdb:kitefin
   ```

5. **Get Database URL:**
   ```bash
   heroku config:get CLEARDB_DATABASE_URL
   # Parse the URL and set individual variables
   ```

6. **Set Environment Variables:**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=30
   # Set DB variables from the database URL
   ```

7. **Create `Procfile`:**
   ```
   web: alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

8. **Deploy:**
   ```bash
   git push heroku main
   ```

---

### AWS (EC2 + RDS)

For production deployments on AWS.

#### Steps:

1. **Create RDS MySQL Instance:**
   - Go to AWS RDS Console
   - Create MySQL 8.0 instance
   - Note: Master username, password, endpoint, and port

2. **Launch EC2 Instance:**
   - Use Ubuntu 22.04 LTS
   - Configure security group to allow:
     - SSH (port 22) from your IP
     - HTTP (port 80) from anywhere
     - HTTPS (port 443) from anywhere
     - Custom TCP (port 8000) if needed

3. **Connect to EC2:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

4. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv mysql-client -y
   ```

5. **Clone and Setup:**
   ```bash
   git clone https://github.com/Beepeen78/expense_tracker.git
   cd expense_tracker
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure Environment:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with RDS credentials
   ```

7. **Run Migrations:**
   ```bash
   alembic upgrade head
   ```

8. **Install and Configure Nginx (Optional):**
   ```bash
   sudo apt install nginx -y
   # Configure nginx as reverse proxy
   ```

9. **Run with Systemd:**
   Create `/etc/systemd/system/expense-tracker.service`:
   ```ini
   [Unit]
   Description=Expense Tracker API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/expense_tracker
   Environment="PATH=/home/ubuntu/expense_tracker/venv/bin"
   ExecStart=/home/ubuntu/expense_tracker/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable expense-tracker
   sudo systemctl start expense-tracker
   ```

---

### DigitalOcean

[DigitalOcean](https://www.digitalocean.com) offers App Platform and Droplets.

#### Using App Platform:

1. **Create App:**
   - Connect GitHub repository
   - Select "Web Service"

2. **Configure:**
   - Build Command: `pip install -r requirements.txt && alembic upgrade head`
   - Run Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Managed Database:**
   - Create MySQL database
   - Use connection string in environment variables

4. **Set Environment Variables:**
   - Add all required variables from `.env.example`

#### Using Droplets (Similar to AWS EC2):

Follow the AWS EC2 steps above, but use DigitalOcean Droplets instead.

---

### Fly.io

[Fly.io](https://fly.io) offers global deployment with edge computing.

#### Steps:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Create App:**
   ```bash
   fly launch
   ```

4. **Create `fly.toml`:**
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]

   [env]
     PORT = "8000"

   [[services]]
     internal_port = 8000
     protocol = "tcp"

     [[services.ports]]
       handlers = ["http"]
       port = 80

     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

5. **Add MySQL Database:**
   ```bash
   fly postgres create --name expense-tracker-db
   # Or use external MySQL service
   ```

6. **Set Secrets:**
   ```bash
   fly secrets set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   fly secrets set DB_USER=your_user
   fly secrets set DB_PASSWORD=your_password
   # ... set all required variables
   ```

7. **Deploy:**
   ```bash
   fly deploy
   ```

---

## Post-Deployment

### 1. Verify Deployment

- Check API health: `https://your-domain.com/`
- Access API docs: `https://your-domain.com/docs`
- Test authentication: Create a user and login

### 2. Security Checklist

- [ ] Changed `SECRET_KEY` to a strong random value
- [ ] Database credentials are secure
- [ ] HTTPS is enabled (if using custom domain)
- [ ] Environment variables are set correctly
- [ ] Database is not publicly accessible (use firewall rules)
- [ ] CORS is configured if needed (add to FastAPI app)

### 3. Add CORS (if needed)

If you need to access the API from a frontend, add CORS middleware in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Monitoring

Consider adding:
- **Logging:** Configure proper logging
- **Health checks:** Add `/health` endpoint
- **Monitoring:** Use services like Sentry, Datadog, or New Relic

### 5. Database Backups

- Set up automated backups for your database
- Most cloud providers offer automated backup solutions

---

## Troubleshooting

### Database Connection Issues

- Verify database credentials
- Check firewall rules (database should allow connections from your app)
- Ensure database is running and accessible

### Migration Issues

- Run `alembic upgrade head` manually if needed
- Check Alembic version history: `alembic history`

### Port Issues

- Ensure the port is correctly configured
- Some platforms use `$PORT` environment variable

---

## Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## Support

For issues or questions, please open an issue on [GitHub](https://github.com/Beepeen78/expense_tracker/issues).

