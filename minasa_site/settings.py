import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-a-secure-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'quizzes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'minasa_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'minasa_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration: default to console backend for development.
# For production, set environment variables (see .env.example / README.md).
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)

# Default from address (used by send_mail)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'katrinamicaellabarbosa@gmail.com')

# If the SMTP backend is selected, read SMTP credentials from environment variables.
if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = os.environ.get('SMTP_HOST')
    EMAIL_PORT = int(os.environ.get('SMTP_PORT', 587))
    EMAIL_HOST_USER = os.environ.get('SMTP_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
    # Prefer TLS on port 587; use SSL on port 465 if required by provider
    EMAIL_USE_TLS = os.environ.get('SMTP_USE_TLS', 'True').lower() in ('1', 'true', 'yes')
    EMAIL_USE_SSL = os.environ.get('SMTP_USE_SSL', 'False').lower() in ('1', 'true', 'yes')
    # Optional timeout (seconds)
    try:
        EMAIL_TIMEOUT = int(os.environ.get('SMTP_TIMEOUT', 10))
    except Exception:
        EMAIL_TIMEOUT = 10

    # Security note: do NOT commit real credentials into source control. Use environment
    # variables, a secrets manager, or a local .env file loaded by your process manager.
