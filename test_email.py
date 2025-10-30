"""
Test Email Sending - Django Project
This script tests if email configuration is working correctly
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("  EMAIL CONFIGURATION TEST")
print("=" * 60)
print()

# Display current configuration
print("📧 Current Email Settings:")
print(f"  Backend: {settings.EMAIL_BACKEND}")
print(f"  Host: {settings.EMAIL_HOST}")
print(f"  Port: {settings.EMAIL_PORT}")
print(f"  User: {settings.EMAIL_HOST_USER}")
print(f"  From: {settings.DEFAULT_FROM_EMAIL}")
print(f"  TLS: {settings.EMAIL_USE_TLS}")
print(f"  Password Set: {bool(settings.EMAIL_HOST_PASSWORD)}")
print()

# Ask for test email address
print("=" * 60)
test_email = input("Enter your email address to receive a test email: ").strip()

if not test_email or '@' not in test_email:
    print("❌ Invalid email address. Exiting.")
    exit(1)

print()
print(f"📤 Sending test email to: {test_email}")
print("Please wait...")
print()

try:
    result = send_mail(
        subject='🧪 Test Email from Django - Minasa Learning Platform',
        message='This is a test email from your Django project. If you receive this, email sending is configured correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    
    if result == 1:
        print("✅ ✅ ✅ EMAIL SENT SUCCESSFULLY! ✅ ✅ ✅")
        print()
        print(f"Check your inbox at: {test_email}")
        print("(Don't forget to check spam/junk folder if you don't see it)")
        print()
        print("🎉 Email configuration is working perfectly!")
        print()
        print("=" * 60)
        print("  YOU'RE ALL SET!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Start your Django server: python manage.py runserver")
        print("2. Create a new user account via signup")
        print("3. Check the registered email for temporary password")
        print("4. Login and change password")
        print("5. Enjoy your new dashboard!")
        print()
    else:
        print("❌ Email sending failed (returned 0)")
        
except Exception as e:
    print("❌ ❌ ❌ ERROR SENDING EMAIL ❌ ❌ ❌")
    print()
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print()
    print("Common issues:")
    print("1. Check if App Password is correct")
    print("2. Verify Gmail account allows SMTP access")
    print("3. Check internet connection")
    print("4. Make sure 2-Step Verification is enabled on Gmail")
    print()
