# 📧 Email Configuration Guide for Sending Temporary Passwords

## Overview
Your Django project is now configured to send **real emails** using Gmail's SMTP server. Temporary passwords will be sent to users' registered email addresses during signup.

---

## 🔐 Step 1: Generate a Gmail App Password

Since Gmail requires 2-Step Verification for app access, you need to create an **App Password**:

### Instructions:

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Under "How you sign in to Google", click **2-Step Verification**
   - Follow the prompts to enable it

2. **Generate an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Windows Computer** (or other)
   - Click **Generate**
   - Copy the 16-character password (it looks like: `xxxx xxxx xxxx xxxx`)

3. **Save this password** - you'll need it in the next step!

---

## ⚙️ Step 2: Set Environment Variable (Windows PowerShell)

To securely store your App Password, set it as an environment variable:

### Option A: Set for Current PowerShell Session (Temporary)
```powershell
$env:SMTP_PASSWORD = "your-16-character-app-password"
```

### Option B: Set System-Wide (Permanent)
```powershell
# Run PowerShell as Administrator, then:
[System.Environment]::SetEnvironmentVariable('SMTP_PASSWORD', 'your-16-character-app-password', 'User')
```

**Replace** `your-16-character-app-password` with the actual App Password from Step 1.

---

## ✅ Step 3: Verify Configuration

After setting the environment variable, restart your Django server:

```powershell
python manage.py runserver
```

Then test email sending by:
1. Creating a new user account via the signup page
2. Check the registered email inbox for the temporary password
3. You should receive an email with subject: **"Your Temporary Password"**

---

## 🧪 Step 4: Test Email in Python Console (Optional)

You can test email sending directly:

```powershell
python manage.py shell
```

Then run:
```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test message from your Django app!',
    'katrinamicaellabarbosa@gmail.com',  # From email
    ['recipient@example.com'],  # To email (use your real email)
    fail_silently=False,
)
```

If successful, you'll see `1` returned, and the email will arrive!

---

## 🔧 Current Settings (in settings.py)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'katrinamicaellabarbosa@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # From environment variable
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'katrinamicaellabarbosa@gmail.com'
```

---

## ⚠️ Troubleshooting

### Issue: "SMTPAuthenticationError: Username and Password not accepted"
**Solution**: 
- Make sure you're using the **App Password**, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check that the environment variable is set correctly

### Issue: Email not received
**Solution**:
- Check spam/junk folder
- Verify the recipient email is correct
- Check server logs for errors

### Issue: "SMTPServerDisconnected: Connection unexpectedly closed"
**Solution**:
- Check your internet connection
- Gmail might be temporarily blocking. Wait a few minutes and try again

---

## 🔒 Security Notes

- **Never commit** your App Password to Git
- Use environment variables for sensitive data
- The App Password is specific to this application
- You can revoke it anytime at: https://myaccount.google.com/apppasswords

---

## 📝 How It Works Now

### Signup Flow:
1. User fills signup form with email, username, password, etc.
2. Django creates user account
3. **Temporary password is generated** (random 8-character string)
4. **Email is sent** to the registered email address with the temp password
5. User receives email and can login with temporary password
6. User is prompted to **change password** on first login
7. After changing password, user is redirected to **Dashboard**

### Email Template:
```
Subject: Your Temporary Password

Hello [username],

Your account has been created successfully!

Your temporary password is: [8-character-code]

Please log in at http://127.0.0.1:8000/login/ and change your password immediately.

Thank you!
```

---

## 📊 Dashboard Features

After successful login and password change, users will see:
- **Welcome message** with their name
- **Profile card** showing username, grade, email
- **Learning progress** (lessons completed, quiz scores)
- **Quick actions** (Browse Lessons, Take Quiz, Festival Tour)
- **Recent activity** feed
- **Learning paths** with direct links to lessons and festival

---

## 🎯 Next Steps

1. Generate Gmail App Password
2. Set `SMTP_PASSWORD` environment variable
3. Restart Django server
4. Test signup with a real email address
5. Check email inbox for temporary password
6. Login and change password
7. Enjoy the new dashboard!

---

## Need Help?

If you encounter issues:
1. Check the Django server console for error messages
2. Verify all environment variables are set
3. Test with the Python shell method above
4. Make sure Gmail hasn't blocked the login attempt (check security alerts)

Good luck! 🚀
