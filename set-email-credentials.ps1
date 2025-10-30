# Quick setup script for your email credentials
# This will set the environment variable for your Django project

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Setting up Email Credentials" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set the environment variable
$env:SMTP_PASSWORD = "sfxr wvap lbwj bszs"

Write-Host "✅ Environment variable SMTP_PASSWORD set for current session!" -ForegroundColor Green
Write-Host ""
Write-Host "Email Configuration:" -ForegroundColor Yellow
Write-Host "  Email: coffeecornerofficial1@gmail.com" -ForegroundColor White
Write-Host "  Password: sfxr wvap lbwj bszs (App Password)" -ForegroundColor White
Write-Host "  Host: smtp.gmail.com" -ForegroundColor White
Write-Host "  Port: 587" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Ready to Send Emails!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: You need to restart your Django server for changes to take effect." -ForegroundColor Yellow
Write-Host ""
Write-Host "Run these commands:" -ForegroundColor Green
Write-Host "  cd C:\Users\Administrator\Documents\project-main\project-main" -ForegroundColor Gray
Write-Host "  python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "Then test by creating a new user account!" -ForegroundColor White
Write-Host ""
