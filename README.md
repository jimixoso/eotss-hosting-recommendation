# EOTSS Hosting Recommendation System

A comprehensive hosting recommendation system for the Executive Office of Technology Services and Security (EOTSS) of the Commonwealth of Massachusetts. This system helps agencies determine the optimal hosting platform for their applications through an intelligent assessment process with automated review workflows.

## 🚀 Features

### Core Assessment System
- **Intelligent Questioning**: 12 targeted questions covering application requirements and cloud readiness
- **Smart Scoring Algorithm**: Analyzes responses to recommend AWS, On-Prem Cloud, or Physical hosting
- **Detailed Explanations**: Provides reasoning for each recommendation
- **Progress Tracking**: Real-time progress indicator during assessment
- **Copy & Print**: Easy sharing of results with copy-to-clipboard and print functionality

### Email Automation & Review Workflow
- **Automated EOTSS Notifications**: Sends detailed assessment results to EOTSS for review
- **Agency Confirmations**: Confirms submission to agencies with ticket ID
- **Professional Review System**: EOTSS can approve or override system recommendations
- **Override Workflow**: Choose alternative hosting options when overriding with mandatory notes
- **Status Tracking**: Complete workflow from submission to final decision
- **Professional Email Templates**: Government-appropriate formatting and branding

### Management & Administration
- **Assessment Dashboard**: Comprehensive view of all submissions with status tracking
- **Review Interface**: Professional form for EOTSS to approve/override assessments
- **File-based Storage**: Simple JSON storage for assessments (production-ready)
- **Unique Identifiers**: Each submission gets both UUID and 8-character ticket ID
- **Clickable Ticket IDs**: Easy navigation to view full assessment details

### Production-Ready Features
- **Docker Deployment**: Complete containerized deployment with Nginx reverse proxy
- **SSL/HTTPS Support**: Production-ready security with SSL certificate configuration
- **Environment Configuration**: Flexible configuration management for different environments
- **Health Checks**: Built-in monitoring and health check endpoints
- **Security Headers**: Comprehensive security configuration
- **Rate Limiting**: Protection against abuse

## 📋 Prerequisites

- Python 3.11+
- Docker (for production deployment)
- SMTP email server access
- Git

## 🛠️ Installation

### Quick Start (Development)
```bash
# Clone the repository
git clone <repository-url>
cd EOTSS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your email settings

# Run the application
python app.py
```

### Production Deployment
```bash
# Clone and setup
git clone <repository-url>
cd EOTSS

# Configure environment variables
cp env.example .env
# Edit .env with production values

# Deploy with Docker
chmod +x deploy.sh
./deploy.sh
```

## 🎯 Usage

### Web Application Workflow

1. **Agency Assessment**:
   - Agency completes the assessment form at `http://localhost:5000`
   - System generates hosting recommendation with detailed reasoning
   - Agency fills out contact information and submits to EOTSS
   - Agency receives confirmation email with ticket ID

2. **EOTSS Review**:
   - EOTSS receives detailed email with assessment results and review link
   - EOTSS accesses review form to approve or override recommendation
   - If overriding: EOTSS selects alternative hosting option and provides mandatory notes
   - Agency receives notification of final decision

3. **Management Dashboard**:
   - Access dashboard at `http://localhost:5000/dashboard`
   - View all assessments with status (pending/approved/overridden)
   - Click ticket IDs to view full assessment details
   - Track alternative recommendations for overridden assessments

### CLI/GUI Tool

The original CLI and GUI versions are still available:

```bash
# CLI version
python eotss_hosting_recommendation_with_app_age.py

# GUI version
python eotss_hosting_recommendation_with_app_age.py --gui
```

## 📁 Project Structure

```
EOTSS/
├── app.py                              # Main Flask web application
├── config.py                           # Configuration management
├── eotss_hosting_recommendation_with_app_age.py  # Original CLI/GUI tool
├── requirements.txt                    # Python dependencies
├── templates/
│   ├── form.html                      # Assessment form with progress tracking
│   ├── result.html                    # Results page with email submission
│   ├── review.html                    # EOTSS review form with override workflow
│   ├── dashboard.html                 # Assessment management dashboard
│   └── view_assessment.html           # Detailed assessment view
├── assessment_data/                   # JSON files storing assessments
├── Dockerfile.prod                    # Production Docker configuration
├── docker-compose.prod.yml            # Multi-container production deployment
├── nginx.prod.conf                    # Production Nginx configuration
├── deploy.sh                          # Automated deployment script
├── env.example                        # Environment variables template
├── PRODUCTION.md                      # Production deployment guide
├── HANDOFF_GUIDE.md                   # Complete handoff documentation
├── QUICK_START.md                     # Quick start guide
└── README.md                          # This file
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file based on `env.example`:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.your-server.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@mass.gov
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@mass.gov
EOTSS_EMAIL=eotss-hosting@mass.gov
DATA_DIR=assessment_data
LOG_LEVEL=INFO
```

### Email Configuration
- **Development**: Use Gmail SMTP with app password
- **Production**: Use EOTSS email server infrastructure
- **Testing**: Configure test email addresses

## 🚀 Deployment Options

### Option 1: Docker Production Deployment (Recommended)
```bash
# Automated deployment
./deploy.sh
```

### Option 2: Manual Server Setup
Follow the detailed guide in `PRODUCTION.md`

### Option 3: Cloud Platform Deployment
- **Heroku**: Use `Procfile` and `requirements.txt`
- **AWS**: Use Docker deployment with ECS/EKS
- **Azure**: Use Docker deployment with Container Instances

## 🔧 Customization

### Assessment Questions
Edit the `QUESTIONS` and `CLOUD_READINESS_QUESTIONS` lists in `app.py` to modify assessment criteria.

### Scoring Algorithm
Update the `score_answers()` function in `app.py` to adjust recommendation logic.

### Email Templates
Modify email functions in `app.py` to customize notification content and formatting.

### Override Options
Update the override workflow in `templates/review.html` to modify alternative recommendation options.

### Styling
The application uses Tailwind CSS. Modify HTML templates to change appearance and branding.

## 🔐 Security Features

- **HTTPS/SSL**: Production-ready SSL configuration
- **Security Headers**: CSP, X-Frame-Options, HSTS, etc.
- **Rate Limiting**: Protection against abuse
- **Non-root Containers**: Secure Docker deployment
- **Environment Variables**: Secure configuration management
- **Input Validation**: Comprehensive form validation

## 📊 Monitoring & Maintenance

### Health Checks
- Application: `http://your-domain/health`
- Docker containers: `docker ps`
- Nginx: `systemctl status nginx`

### Logs
- Application logs: Docker container logs
- Nginx logs: `/var/log/nginx/`
- System logs: `journalctl -u docker`

### Backup
- Assessment data: `assessment_data/` directory
- Configuration: `.env` file
- SSL certificates: `/etc/ssl/` directory

## 🆘 Troubleshooting

### Common Issues
1. **Email not sending**: Check SMTP credentials and server settings
2. **Assessment not saving**: Verify `assessment_data/` directory permissions
3. **SSL errors**: Check certificate paths and renewal dates
4. **Docker issues**: Verify Docker installation and permissions

### Getting Help
- **Quick Start**: See `QUICK_START.md`
- **Production Setup**: See `PRODUCTION.md`
- **Complete Documentation**: See `HANDOFF_GUIDE.md`

## 🎓 Training & Handoff

### For EOTSS Team
- **Development Setup**: See `QUICK_START.md`
- **Production Deployment**: See `PRODUCTION.md`
- **Complete Handoff**: See `HANDOFF_GUIDE.md`

### Recommended Skills
- Python/Flask development
- Docker container management
- Linux server administration
- Git version control
- Email system configuration

## 📈 Future Enhancements

### Short-term
- User authentication for EOTSS dashboard
- Database migration (PostgreSQL/MySQL)
- API development for integrations
- Enhanced reporting and analytics

### Long-term
- Integration with existing EOTSS systems
- Automated assessment processing
- Advanced compliance checking
- Machine learning for recommendations

## 📄 License

This project is developed for the Commonwealth of Massachusetts EOTSS.

## 📞 Support

For technical support or questions about the hosting recommendation system:
- **EOTSS IT Support**: [EOTSS IT contact]
- **System Administrator**: [Server admin contact]
- **Documentation**: See `HANDOFF_GUIDE.md` for complete documentation

---

**Last Updated**: August 2025
**Version**: 2.0 (Production Ready)
**Status**: Ready for EOTSS deployment 
