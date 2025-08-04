# Quick Start Guide - EOTSS Hosting Recommendation System

## 🚀 **Get Running in 5 Minutes**

### **Prerequisites:**
- Python 3.11+ installed
- Git installed
- Email server access (for notifications)

### **Step 1: Clone and Setup**
```bash
git clone [your-repository-url]
cd EOTSS
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **Step 2: Configure Email**
```bash
cp env.example .env
# Edit .env with your email settings:
# MAIL_USERNAME=your-email@mass.gov
# MAIL_PASSWORD=your-password
# EOTSS_EMAIL=eotss-hosting@mass.gov
```

### **Step 3: Run the Application**
```bash
python app.py
```

### **Step 4: Access the System**
- **Assessment Form**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard
- **Review Form**: http://localhost:5000/review/[assessment-id]

## 📋 **Quick Test Workflow**

1. **Submit Assessment**: Fill out the form at http://localhost:5000
2. **Check Dashboard**: View submitted assessment at http://localhost:5000/dashboard
3. **Review Assessment**: Click "Review" button on dashboard
4. **Test Override**: Try overriding the system recommendation
5. **Check Emails**: Verify email notifications are sent

## 🔧 **Common Issues & Solutions**

### **Email Not Working:**
- Check SMTP settings in `.env`
- Verify email credentials
- Test with Gmail SMTP for development

### **Assessment Not Saving:**
- Check `assessment_data/` directory exists
- Verify file permissions
- Check application logs

### **Port Already in Use:**
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9
# Or change port in app.py
```

## 📞 **Need Help?**

- **Full Documentation**: See `HANDOFF_GUIDE.md`
- **Production Setup**: See `PRODUCTION.md`
- **Your Contact**: [Your email/phone during transition]

---

**This guide gets you running quickly. For production deployment, see `PRODUCTION.md`.** 