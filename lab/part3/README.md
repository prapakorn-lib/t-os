# FastAPI Item Management API

Simple REST API for managing items with PostgreSQL database.

## 📋 Requirements

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+
- PostgreSQL 12+
- 2GB RAM minimum
- 10GB disk space

## 🚀 Quick Start

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib -y
```

### 2. Setup PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Run setup script
sudo -u postgres psql -f setup_database.sql
```

### 3. Setup Python Environment

```bash
# Create project directory
mkdir fastapi_project
cd fastapi_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Generate secure API key:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Setup Project Structure

```bash
mkdir -p app
mv database.py models.py main.py app/
mv __init__.py app/
```

### 6. Run Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode with systemd (see guide)
```

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔑 API Endpoints

### Public Endpoints
- `GET /` - API information
- `GET /health` - Health check

### Protected Endpoints (Require API Key)
- `GET /items` - Get all items
- `GET /items/{id}` - Get item by ID

### Authentication

Include API key in header:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/items
```

## 🧪 Testing

```bash
# Test without API key (should return 403)
curl http://localhost:8000/items

# Test with API key
curl -H "X-API-Key: your-api-key" http://localhost:8000/items

# Test specific item
curl -H "X-API-Key: your-api-key" http://localhost:8000/items/1

# Test health check
curl http://localhost:8000/health
```

## 📁 Project Structure

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application
│   ├── database.py     # Database connection
│   └── models.py       # Pydantic models
├── venv/               # Virtual environment
├── .env                # Environment variables (not in git)
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
├── setup_database.sql  # Database setup script
└── README.md          # This file
```

## 🔒 Security

- Keep `.env` file secure and never commit to git
- Use strong passwords for database
- Generate secure API keys
- Configure firewall (UFW)
- Use HTTPS in production

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U apiuser -d apidb -h localhost
```

### Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📝 Development

### Adding New Endpoints

1. Define Pydantic model in `models.py`
2. Add endpoint function in `main.py`
3. Test with Swagger UI
4. Update documentation

### Database Migrations

For schema changes:
```bash
psql -U apiuser -d apidb
# Run ALTER TABLE commands
```

## 🚀 Production Deployment

See `lab-part3-guide.md` section 3.5 for:
- systemd service setup
- Process management
- Monitoring configuration
- Log rotation

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 👥 Support

For issues or questions, refer to the lab guide or contact your instructor.

## 📄 License

This project is for educational purposes (Operating Systems Lab).

---

**Version:** 1.0.0  
**Last Updated:** November 2025
