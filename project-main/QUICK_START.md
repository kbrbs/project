# 🚀 Quick Start: Dashboard & Email Setup

## What's New?

### ✅ Dashboard Page
- **URL**: http://127.0.0.1:8000/dashboard/
- **Features**:
  - Personalized welcome message
  - Profile overview (username, grade, email)
  - Learning progress stats
  - Quick action buttons
  - Recent activity feed
  - Learning paths

### ✅ Email Integration
- Temporary passwords are now **sent to registered email addresses**
- Uses Gmail SMTP server
- Secure App Password authentication

---

## 🎯 New User Flow

```
1. Signup → User enters email, username, password, grade, full name
2. Email Sent → Temporary password sent to registered email
3. Login → User logs in with temporary password
4. Change Password → Required on first login
5. Dashboard → User redirected to personalized dashboard
```

---

## ⚡ Quick Setup (3 Steps)

### Step 1: Get Gmail App Password
```
https://myaccount.google.com/apppasswords
```
- Enable 2-Step Verification
- Generate App Password (Mail → Windows Computer)
- Copy the 16-character password

### Step 2: Run Setup Script
```powershell
cd C:\Users\Administrator\Documents\project-main\project-main
.\setup-email.ps1
```
- Enter your App Password when prompted
- Choose option 2 (permanent setup)

### Step 3: Restart Server
```powershell
python manage.py runserver
```

**Done!** 🎉

---

## 🧪 Testing

### Test Email Sending:
```powershell
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'Testing Django email!',
    'katrinamicaellabarbosa@gmail.com',
    ['your-test-email@example.com'],
    fail_silently=False,
)
```

Expected result: `1` (email sent successfully)

### Test Dashboard:
1. Create user account: http://127.0.0.1:8000/accounts/signup/
2. Check email for temporary password
3. Login: http://127.0.0.1:8000/login/
4. Change password when prompted
5. View dashboard: http://127.0.0.1:8000/dashboard/

---

## 📋 What Changed?

### Files Modified:
1. **core/views.py** - Added `dashboard()` view
2. **core/urls.py** - Added dashboard URL route
3. **templates/core/dashboard.html** - New dashboard template
4. **minasa_site/settings.py** - Changed to SMTP email backend

### Files Created:
1. **EMAIL_SETUP_GUIDE.md** - Detailed setup instructions
2. **setup-email.ps1** - Automated setup script
3. **QUICK_START.md** - This file

---

## 🔍 Verify Email Configuration

Check current settings:
```python
# In Django shell
from django.conf import settings

print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
print(f"Password set: {bool(settings.EMAIL_HOST_PASSWORD)}")
```

Expected output:
```
Backend: django.core.mail.backends.smtp.EmailBackend
Host: smtp.gmail.com
Port: 587
User: katrinamicaellabarbosa@gmail.com
From: katrinamicaellabarbosa@gmail.com
TLS: True
Password set: True
```

---

## 🐛 Common Issues

### Issue 1: "SMTPAuthenticationError"
**Solution**: Use App Password, not regular Gmail password

### Issue 2: Environment variable not found
**Solution**: 
```powershell
# Check if set:
$env:SMTP_PASSWORD

# If empty, set it:
$env:SMTP_PASSWORD = "your-app-password"
```

### Issue 3: Email in spam folder
**Solution**: Check spam/junk folder, mark as "Not Spam"

### Issue 4: Dashboard not found
**Solution**: Make sure you're logged in and server is running

---

## 📧 Email Template

Users will receive:
```
Subject: Your Temporary Password

Hello [username],

Your account has been created successfully!

Your temporary password is: [8-char-code]

Please log in at http://127.0.0.1:8000/login/ 
and change your password immediately.

Thank you!
```

---

## 🎨 Dashboard Features

### Profile Card
- Shows username, grade, email
- Link to full profile page

### Learning Progress
- Lessons completed count
- Quizzes taken count
- Average score

### Quick Actions
- Browse Lessons button
- Take a Quiz button
- Festival Tour button

### Recent Activity
- Shows user's learning history
- Empty state for new users

### Learning Paths
- Explore Lessons card
- Virtual Festival card

---

## 🔐 Security Reminders

- ✅ App Password is stored in environment variable (not in code)
- ✅ Never commit SMTP_PASSWORD to Git
- ✅ App Password can be revoked anytime
- ✅ Use different App Passwords for different apps

---

## 📚 Additional Resources

- **Detailed Setup**: See `EMAIL_SETUP_GUIDE.md`
- **Gmail App Passwords**: https://myaccount.google.com/apppasswords
- **Django Email Docs**: https://docs.djangoproject.com/en/stable/topics/email/

---

## ✨ You're All Set!

Your Django project now has:
- ✅ Beautiful dashboard page
- ✅ Real email sending via Gmail SMTP
- ✅ Temporary password delivery
- ✅ Smooth authentication flow

**Enjoy building!** 🎉
