# EOTSS Hosting Recommendation System

A comprehensive hosting recommendation system for the Executive Office of Technology Services and Security (EOTSS) of the Commonwealth of Massachusetts. This system helps agencies determine the optimal hosting platform for their applications through an intelligent assessment process.

## Features

### Core Assessment System
- **Intelligent Questioning**: 12 targeted questions covering application requirements and cloud readiness
- **Smart Scoring Algorithm**: Analyzes responses to recommend AWS, On-Prem Cloud, or Physical hosting
- **Detailed Explanations**: Provides reasoning for each recommendation
- **Progress Tracking**: Real-time progress indicator during assessment

### Email Automation (Version 2)
- **Automated EOTSS Notifications**: Sends assessment results to EOTSS for review
- **Agency Confirmations**: Confirms submission to agencies
- **Review System**: EOTSS can approve/override assessments with feedback
- **Status Tracking**: Complete workflow from submission to approval
- **Professional Email Templates**: Government-appropriate formatting

### Management Features
- **Assessment Dashboard**: View all submissions and their status
- **Review Interface**: Professional form for EOTSS to approve/override assessments
- **File-based Storage**: Simple JSON storage for assessments (no database required)
- **Unique Assessment IDs**: Each submission gets a unique identifier

## Prerequisites

- Python 3.7+
- Flask
- Flask-Mail
- Gmail account with 2FA enabled (for email functionality)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd EOTSS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email settings** (in `app.py`):
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-gmail-app-password'
   app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
   ```

4. **Set up Gmail App Password**:
   - Enable 2-Factor Authentication on your Gmail account
   - Go to Google Account Settings → Security → App Passwords
   - Generate a password for "Mail"
   - Use this password in the configuration

## Usage

### Web Application

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   - Main form: `http://localhost:5000`
   - Dashboard: `http://localhost:5000/dashboard`

### Complete Workflow

1. **Agency Assessment**:
   - Agency completes the assessment form
   - System generates hosting recommendation
   - Agency fills out contact information
   - Assessment is submitted to EOTSS

2. **EOTSS Review**:
   - EOTSS receives email with assessment details and review link
   - EOTSS clicks link to access review form
   - EOTSS can approve or override with optional comments
   - Agency receives notification of decision

3. **Management**:
   - Use dashboard to view all assessments
   - Track status (pending/approved/overridden)
   - Access review forms for pending assessments

### CLI/GUI Tool

The original CLI and GUI versions are still available:

```bash
# CLI version
python eotss_hosting_recommendation_with_app_age.py

# GUI version
python eotss_hosting_recommendation_with_app_age.py --gui
```

## Project Structure

```
EOTSS/
├── app.py                              # Flask web application
├── eotss_hosting_recommendation_with_app_age.py  # Original CLI/GUI tool
├── requirements.txt                    # Python dependencies
├── templates/
│   ├── form.html                      # Assessment form
│   ├── result.html                    # Results page with email submission
│   ├── review.html                    # EOTSS review form
│   └── dashboard.html                 # Assessment management dashboard
├── assessment_data/                   # JSON files storing assessments
├── Dockerfile                         # Docker configuration
├── Procfile                          # Heroku deployment
├── nginx.conf                        # Nginx configuration
└── README.md                         # This file
```

## Email Configuration

### For Demo/Testing
- **EOTSS Email**: `jimixoso@mit.edu` (configurable in `app.py`)
- **Agency Email**: Whatever email they enter in the contact form
- **SMTP**: Gmail SMTP (smtp.gmail.com:587)

### For Production
- Update email credentials to use EOTSS email server
- Configure proper domain and security settings
- Update review URLs to use production domain

## Deployment

### Local Development
```bash
python app.py
```

### Docker Deployment
```bash
docker build -t eotss-hosting .
docker run -p 8000:8000 eotss-hosting
```

### Production Deployment
1. Set up a production server
2. Configure Nginx as reverse proxy
3. Use Gunicorn as WSGI server
4. Set up proper SSL certificates
5. Configure production email settings

## Customization

### Adding Questions
Edit the `QUESTIONS` and `CLOUD_READINESS_QUESTIONS` lists in `app.py` to add or modify assessment questions.

### Modifying Scoring
Update the `score_answers()` function to adjust the recommendation algorithm.

### Email Templates
Modify the email functions (`send_eotss_notification`, `send_agency_confirmation`, `send_review_notification`) to customize email content.

### Styling
The application uses Tailwind CSS. Modify the HTML templates to change the appearance.

## Security Considerations

- **Secret Key**: Change the `SECRET_KEY` in production
- **Email Credentials**: Use environment variables for sensitive data
- **File Permissions**: Ensure `assessment_data/` directory has proper permissions
- **HTTPS**: Use SSL/TLS in production

## Troubleshooting

### Email Issues
- Ensure 2FA is enabled on Gmail
- Verify app password is correct
- Check firewall settings for SMTP ports

### Assessment Not Saving
- Ensure `assessment_data/` directory exists and is writable
- Check file permissions

### Review Links Not Working
- Verify the application is running on the correct port
- Check that assessment IDs are being generated correctly

## License

This project is developed for the Commonwealth of Massachusetts EOTSS.

## Support

For technical support or questions about the hosting recommendation system, contact the EOTSS team, and Jimi Oso. 
