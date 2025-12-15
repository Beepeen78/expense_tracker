# Quick Start Deployment Guide

## 🚀 Fastest Way to Deploy

### Option 1: Docker Compose (Local/Development)

```bash
# 1. Clone the repository
git clone https://github.com/Beepeen78/expense_tracker.git
cd expense_tracker

# 2. Create .env file
cp .env.example .env
# Edit .env and set SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")

# 3. Start everything
docker-compose up -d

# 4. Access API
# http://localhost:8000/docs
```

### Option 2: Railway (Recommended for Production)

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add MySQL database: "New" → "Database" → "MySQL"
5. Set environment variables (from MySQL service + SECRET_KEY)
6. Deploy automatically!

**See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.**

---

## 📋 Environment Variables Required

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=3306
DB_NAME=expense_tracker
SECRET_KEY=your_secure_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🔗 Deployment Platforms

- **Railway** - Easiest, automatic deployments
- **Render** - Free tier available
- **Heroku** - Classic PaaS
- **AWS** - Full control, scalable
- **DigitalOcean** - Simple and affordable
- **Fly.io** - Global edge deployment

**Full instructions in [DEPLOYMENT.md](./DEPLOYMENT.md)**

---

## ✅ Post-Deployment Checklist

- [ ] Set strong SECRET_KEY
- [ ] Database credentials configured
- [ ] API accessible at your domain
- [ ] Test authentication (create user, login)
- [ ] Database migrations completed
- [ ] HTTPS enabled (for production)

---

## 🆘 Need Help?

See the comprehensive [DEPLOYMENT.md](./DEPLOYMENT.md) guide for:
- Detailed platform-specific instructions
- Troubleshooting tips
- Security best practices
- Monitoring setup

