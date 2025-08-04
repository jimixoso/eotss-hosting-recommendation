# EOTSS Hosting Recommendation System - Production Deployment Guide

This guide provides step-by-step instructions for deploying the EOTSS Hosting Recommendation System to production.

## 🏗️ Architecture Overview

The production deployment uses:
- **Docker** for containerization
- **Nginx** as reverse proxy with SSL termination
- **Gunicorn** as WSGI server
- **Environment variables** for configuration
- **SSL/TLS** for secure communication

## 📋 Prerequisites

### Server Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 10GB minimum
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Domain & SSL
- **Domain name** pointing to your server
- **SSL certificates** (Let's Encrypt recommended)

## 🚀 Deployment Steps

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd EOTSS
git checkout email-automation-feature
```

### 2. Configure Environment Variables
```bash
# Copy example environment file
cp env.example .env

# Edit with your production values
nano .env
```

**Required Environment Variables:**
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=no-reply@mass.gov
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=no-reply@mass.gov
EOTSS_EMAIL=eotss-hosting@mass.gov
```

### 3. SSL Certificate Setup

#### Option A: Let's Encrypt (Recommended)
```bash
# Install Certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to ssl directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*
```

#### Option B: Self-Signed (Testing Only)
```bash
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem -out ssl/cert.pem
```

### 4. Deploy Application
```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 5. Verify Deployment
```bash
# Check application health
curl https://your-domain.com/health

# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Configuration Options

### Email Server Configuration

#### Microsoft 365 (Recommended for EOTSS)
```bash
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=no-reply@mass.gov
MAIL_PASSWORD=your-app-password
```

#### Gmail (Development/Testing)
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Data Storage
Assessment data is stored in a Docker volume. To backup:
```bash
# Create backup
docker run --rm -v eotss_assessment_data:/data -v $(pwd):/backup alpine tar czf /backup/assessment_data_backup.tar.gz -C /data .

# Restore backup
docker run --rm -v eotss_assessment_data:/data -v $(pwd):/backup alpine tar xzf /backup/assessment_data_backup.tar.gz -C /data
```

## 🔒 Security Considerations

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (redirect to HTTPS)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### SSL/TLS Security
- Use strong SSL certificates
- Enable HSTS headers
- Configure secure cipher suites
- Regular certificate renewal

### Application Security
- Change default SECRET_KEY
- Use strong passwords
- Regular security updates
- Monitor logs for suspicious activity

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Application health
curl https://your-domain.com/health

# Container health
docker-compose -f docker-compose.prod.yml ps
```

### Log Monitoring
```bash
# Application logs
docker-compose -f docker-compose.prod.yml logs -f app

# Nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Backup Strategy
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker run --rm -v eotss_assessment_data:/data -v /backups:/backup alpine \
    tar czf /backup/assessment_data_$DATE.tar.gz -C /data .
```

## 🔄 Updates & Maintenance

### Application Updates
```bash
# Pull latest code
git pull origin email-automation-feature

# Rebuild and restart
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

### SSL Certificate Renewal
```bash
# Let's Encrypt renewal
sudo certbot renew

# Copy renewed certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
sudo chown $USER:$USER ssl/*

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

## 🆘 Troubleshooting

### Common Issues

#### Application Not Starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs app

# Check environment variables
docker-compose -f docker-compose.prod.yml exec app env | grep MAIL
```

#### Email Not Sending
```bash
# Test email configuration
docker-compose -f docker-compose.prod.yml exec app python -c "
from app import mail
print('Mail server:', mail.server)
print('Mail port:', mail.port)
print('Mail TLS:', mail.use_tls)
"
```

#### SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Test SSL connection
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

## 📞 Support

For technical support or questions about the hosting recommendation system, contact the EOTSS team.

### Emergency Contacts
- **EOTSS Support**: eotss-support@mass.gov
- **System Administrator**: [Your Contact Info]
- **Emergency Hotline**: [Emergency Number]

## 📋 Compliance Notes

This system is designed for use by the Commonwealth of Massachusetts and should comply with:
- **Massachusetts Data Security Law** (201 CMR 17.00)
- **EOTSS Security Standards**
- **Commonwealth IT Policies**

Ensure all data handling and security measures meet Commonwealth requirements. 