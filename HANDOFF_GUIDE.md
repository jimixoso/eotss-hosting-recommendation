# EOTSS Hosting Recommendation System - Handoff Guide

## 🎯 **Project Overview**

This system helps Massachusetts state agencies determine the optimal hosting platform for their applications by assessing technical requirements, compliance needs, and operational constraints.

### **Key Features:**
- Web-based assessment form with intelligent scoring
- Automated email notifications to EOTSS and agencies
- EOTSS review workflow with override capabilities
- Dashboard for managing all assessments
- Production-ready deployment with Docker

## 🏗️ **System Architecture**

### **Technology Stack:**
- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript with Tailwind CSS
- **Email**: Flask-Mail with SMTP
- **Storage**: JSON files (can be upgraded to database)
- **Deployment**: Docker with Nginx reverse proxy

### **Key Files:**
- `app.py` - Main Flask application
- `config.py` - Configuration management
- `templates/` - HTML templates
- `assessment_data/` - JSON storage for assessments
- `Dockerfile.prod` - Production Docker image
- `docker-compose.prod.yml` - Multi-container deployment

## 🚀 **Deployment Options**

### **Option 1: Simple Docker Deployment (Recommended)**
```bash
# Clone repository
git clone [repository-url]
cd EOTSS

# Set up environment variables
cp env.example .env
# Edit .env with your production values

# Deploy
chmod +x deploy.sh
./deploy.sh
```

### **Option 2: Manual Server Setup**
- Install Python 3.11+, Nginx, SSL certificates
- Follow `PRODUCTION.md` for detailed instructions

## ⚙️ **Configuration Management**

### **Environment Variables (Required):**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.your-server.com
MAIL_USERNAME=your-email@mass.gov
MAIL_PASSWORD=your-password
EOTSS_EMAIL=eotss-hosting@mass.gov
```

### **Email Configuration:**
- Configure SMTP server details in `.env`
- Test email functionality before production
- Consider using EOTSS's email infrastructure

## 🔧 **Maintenance Tasks**

### **Regular Maintenance:**
1. **Backup Assessment Data**: Daily backups of `assessment_data/` directory
2. **Monitor Logs**: Check application and Nginx logs for errors
3. **Update Dependencies**: Monthly security updates for Python packages
4. **SSL Certificate Renewal**: Every 90 days (if using Let's Encrypt)

### **Data Management:**
- Assessment data stored in JSON files in `assessment_data/`
- Each assessment has unique UUID and ticket ID
- Consider migrating to database for large-scale deployment

## 🛠️ **Development Workflow**

### **Setting Up Development Environment:**
```bash
# Clone repository
git clone [repository-url]
cd EOTSS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env for development

# Run application
python app.py
```

### **Making Changes:**
1. Create feature branch: `git checkout -b feature-name`
2. Make changes and test locally
3. Commit changes: `git commit -m "Description"`
4. Push to repository: `git push origin feature-name`
5. Create pull request for review

## 📊 **Monitoring and Troubleshooting**

### **Health Checks:**
- Application: `http://your-domain/health`
- Docker containers: `docker ps`
- Nginx: `systemctl status nginx`

### **Common Issues:**
1. **Email not sending**: Check SMTP credentials and server settings
2. **Assessment not saving**: Check file permissions on `assessment_data/`
3. **SSL errors**: Verify certificate paths and renewal dates
4. **Performance issues**: Monitor server resources and logs

### **Log Locations:**
- Application logs: Docker container logs
- Nginx logs: `/var/log/nginx/`
- System logs: `journalctl -u docker`

## 🔐 **Security Considerations**

### **Current Security Features:**
- HTTPS/SSL encryption
- Security headers (CSP, X-Frame-Options, etc.)
- Rate limiting on Nginx
- Non-root Docker containers
- Environment variable configuration

### **Recommended Security Enhancements:**
1. **Database**: Migrate from JSON files to PostgreSQL/MySQL
2. **Authentication**: Add user authentication for EOTSS dashboard
3. **Audit Logging**: Log all assessment submissions and reviews
4. **Backup Encryption**: Encrypt backup files
5. **Network Security**: Configure firewall rules

## 📈 **Scaling Considerations**

### **Current Limitations:**
- File-based storage (not suitable for high volume)
- Single server deployment
- No user authentication

### **Scaling Options:**
1. **Database Migration**: Replace JSON files with PostgreSQL
2. **Load Balancing**: Add multiple application servers
3. **Caching**: Implement Redis for session management
4. **CDN**: Add content delivery network for static files

## 📞 **Support and Contact**

### **Emergency Contacts:**
- **Technical Issues**: [Your contact info during transition]
- **EOTSS IT Support**: [EOTSS IT contact]
- **System Administrator**: [Server admin contact]

### **Documentation Resources:**
- `README.md` - General project information
- `PRODUCTION.md` - Production deployment guide
- `requirements.txt` - Python dependencies
- `Dockerfile.prod` - Container configuration

## 🎓 **Training Recommendations**

### **For EOTSS Team:**
1. **Basic Python/Flask**: Understanding the codebase
2. **Docker**: Container management and deployment
3. **Git**: Version control and collaboration
4. **Linux Administration**: Server maintenance
5. **Email Systems**: SMTP configuration and troubleshooting

### **Recommended Training Resources:**
- Python Flask documentation
- Docker official tutorials
- Git and GitHub guides
- Linux server administration courses

## 🔄 **Future Development Ideas**

### **Short-term Enhancements:**
1. **User Authentication**: Add login system for EOTSS staff
2. **Database Integration**: Migrate to PostgreSQL
3. **API Development**: Create REST API for integrations
4. **Reporting**: Add assessment analytics and reporting

### **Long-term Features:**
1. **Integration**: Connect with existing EOTSS systems
2. **Automation**: Automated assessment processing
3. **Compliance**: Enhanced compliance checking
4. **Analytics**: Advanced reporting and dashboards

---

**Last Updated**: [Date]
**Handoff By**: [Your Name]
**Next Review**: [Date] 