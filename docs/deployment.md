# Deployment Documentation

## Overview

This guide covers deploying the LoanLess microloan platform to production environments including cloud platforms, VPS, and containerized deployments.

## Prerequisites

- Python 3.8+
- Git
- Domain name (optional)
- SSL certificate (recommended)

## Environment Setup

### 1. Production Dependencies

```bash
pip install -r backend/requirements.txt
pip install gunicorn  # WSGI server
pip install psycopg2  # PostgreSQL (if using)
```

### 2. Environment Variables

Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=sqlite:///production.db
UPLOAD_FOLDER=/var/www/loanless/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### 3. Production Configuration

Update `app.py`:
```python
import os
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    DEBUG=False,
    TESTING=False
)
```

## Cloud Deployment

### Heroku Deployment

1. **Create Heroku App**
```bash
heroku create loanless-app
heroku addons:create heroku-postgresql:mini
```

2. **Configure Environment**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

3. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
heroku run python backend/migrate_database.py
```

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx supervisor -y

# Clone repository
git clone https://github.com/yourusername/loanless.git
cd loanless
pip3 install -r backend/requirements.txt
```

3. **Configure Nginx**
Create `/etc/nginx/sites-available/loanless`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/ubuntu/loanless/backend/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

4. **Configure Supervisor**
Create `/etc/supervisor/conf.d/loanless.conf`:
```ini
[program:loanless]
command=/usr/bin/python3 /home/ubuntu/loanless/backend/app.py
directory=/home/ubuntu/loanless
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/loanless.log
```

### DigitalOcean Deployment

1. **Create Droplet**
   - Ubuntu 20.04
   - Basic plan ($5/month minimum)
   - Add SSH key

2. **Setup Script**
```bash
#!/bin/bash
# Deploy script for DigitalOcean

# System setup
apt update && apt upgrade -y
apt install python3 python3-pip nginx certbot python3-certbot-nginx -y

# Application setup
cd /var/www
git clone https://github.com/yourusername/loanless.git
cd loanless
pip3 install -r backend/requirements.txt

# Database initialization
python3 backend/migrate_database.py

# SSL Certificate
certbot --nginx -d your-domain.com

# Start services
systemctl enable nginx
systemctl start nginx
```

## VPS/Dedicated Server

### 1. Server Configuration

```bash
# Create user
sudo adduser loanless
sudo usermod -aG sudo loanless

# Switch to app user
sudo su - loanless

# Install application
git clone https://github.com/yourusername/loanless.git
cd loanless
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Systemd Service

Create `/etc/systemd/system/loanless.service`:
```ini
[Unit]
Description=LoanLess Web Application
After=network.target

[Service]
User=loanless
Group=loanless
WorkingDirectory=/home/loanless/loanless
Environment=PATH=/home/loanless/loanless/venv/bin
ExecStart=/home/loanless/loanless/venv/bin/gunicorn --bind 127.0.0.1:5000 backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable loanless
sudo systemctl start loanless
```

## Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY instance/ ./instance/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: loanless
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

## Database Migration

### PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database
sudo -u postgres createdb loanless
sudo -u postgres createuser loanless_user

# Update connection string
DATABASE_URL=postgresql://loanless_user:password@localhost/loanless
```

### Migration Script

```python
# migrate_to_postgres.py
import os
import sqlite3
import psycopg2
from sqlalchemy import create_engine

def migrate_database():
    # Export from SQLite
    sqlite_conn = sqlite3.connect('instance/database.db')
    
    # Import to PostgreSQL
    pg_conn = psycopg2.connect(os.environ['DATABASE_URL'])
    
    # Migration logic here
    print("Database migrated successfully")
```

## SSL Certificate

### Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Manual SSL

1. Purchase SSL certificate
2. Configure Nginx:
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
}
```

## Monitoring & Maintenance

### 1. Log Management

```bash
# Application logs
tail -f /var/log/loanless.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. Health Checks

```python
# health_check.py
import requests
import sys

def check_health():
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("Application is healthy")
            sys.exit(0)
        else:
            print("Application is unhealthy")
            sys.exit(1)
    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_health()
```

### 3. Backup Strategy

```bash
#!/bin/bash
# backup.sh

# Database backup
pg_dump loanless > backups/db_$(date +%Y%m%d_%H%M%S).sql

# File backup
tar -czf backups/files_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# Cleanup old backups (keep 30 days)
find backups/ -name "*.sql" -mtime +30 -delete
find backups/ -name "*.tar.gz" -mtime +30 -delete
```

## Security Hardening

### 1. Firewall Configuration

```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Application Security

```python
# Security headers
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

2. **Permission Denied**
```bash
sudo chown -R loanless:loanless /var/www/loanless
sudo chmod -R 755 /var/www/loanless
```

3. **Database Connection Error**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql
sudo systemctl restart postgresql
```

### Performance Tuning

1. **Nginx Optimization**
```nginx
worker_processes auto;
worker_connections 1024;

gzip on;
gzip_types text/css application/javascript image/svg+xml;

client_max_body_size 16M;
```

2. **Gunicorn Configuration**
```bash
gunicorn --workers 4 --bind 127.0.0.1:5000 --timeout 120 backend.app:app
```

## Rollback Strategy

### Quick Rollback

```bash
#!/bin/bash
# rollback.sh

# Stop application
sudo systemctl stop loanless

# Restore previous version
git checkout previous-working-commit

# Restore database if needed
psql loanless < backups/latest_backup.sql

# Start application
sudo systemctl start loanless
```

## Scaling

### Load Balancer Setup

```nginx
upstream loanless_app {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    location / {
        proxy_pass http://loanless_app;
    }
}
```

### Database Scaling

1. **Read Replicas**: For read-heavy workloads
2. **Connection Pooling**: PgBouncer for PostgreSQL
3. **Caching**: Redis for session storage

This deployment guide covers the essential steps for getting LoanLess running in production. Choose the deployment method that best fits your infrastructure requirements and budget.