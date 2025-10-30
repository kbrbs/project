# Quick Email Setup Script for Windows PowerShell
# This script helps you set up Gmail SMTP for sending temporary passwords

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Django Email Configuration Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will help you configure Gmail SMTP for your Django project." -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANT: Before continuing, you need a Gmail App Password!" -ForegroundColor Red
Write-Host ""
Write-Host "Steps to get your App Password:" -ForegroundColor Green
Write-Host "1. Go to: https://myaccount.google.com/apppasswords" -ForegroundColor White
Write-Host "2. Enable 2-Step Verification if not already enabled" -ForegroundColor White
Write-Host "3. Generate an App Password (select 'Mail' and your device)" -ForegroundColor White
Write-Host "4. Copy the 16-character password" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Do you have your Gmail App Password ready? (y/n)"

if ($continue -ne 'y' -and $continue -ne 'Y') {
    Write-Host ""
    Write-Host "Please generate your App Password first, then run this script again." -ForegroundColor Yellow
    Write-Host "See EMAIL_SETUP_GUIDE.md for detailed instructions." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Great! Let's set up your email configuration." -ForegroundColor Green
Write-Host ""

# Get the App Password
$appPassword = Read-Host "Enter your 16-character Gmail App Password (spaces will be removed)"

# Remove spaces from the password
$appPassword = $appPassword -replace '\s', ''

if ($appPassword.Length -eq 0) {
    Write-Host ""
    Write-Host "Error: No password entered. Exiting." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Choose how to set the environment variable:" -ForegroundColor Cyan
Write-Host "1. Current session only (temporary - for testing)" -ForegroundColor White
Write-Host "2. User-level (permanent - recommended)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1 or 2)"

if ($choice -eq '1') {
    # Set for current session
    $env:SMTP_PASSWORD = $appPassword
    Write-Host ""
    Write-Host "✓ Environment variable set for current PowerShell session!" -ForegroundColor Green
    Write-Host ""
    Write-Host "NOTE: This is temporary. The variable will be lost when you close PowerShell." -ForegroundColor Yellow
    Write-Host "Run this script again and choose option 2 for permanent setup." -ForegroundColor Yellow
}
elseif ($choice -eq '2') {
    # Set at user level (permanent)
    [System.Environment]::SetEnvironmentVariable('SMTP_PASSWORD', $appPassword, 'User')
    Write-Host ""
    Write-Host "✓ Environment variable set permanently for your user account!" -ForegroundColor Green
    Write-Host ""
    Write-Host "NOTE: You need to restart PowerShell and your Django server for changes to take effect." -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "Invalid choice. Exiting." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Restart your Django development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Test email by creating a new user account" -ForegroundColor White
Write-Host ""
Write-Host "3. Check your email inbox for the temporary password!" -ForegroundColor White
Write-Host ""
Write-Host "4. Login, change password, and access your dashboard" -ForegroundColor White
Write-Host ""
Write-Host "For troubleshooting, see EMAIL_SETUP_GUIDE.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
Write-Host ""
