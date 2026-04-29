import os
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# .env'den şifreyi okur, bulamazsa hata vermemesi için sahte bir şifre atar
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# .env'den gelen değer string olduğu için onu Python boolean türüne çeviriyoruz
# Mevcut satırın (Buna dokunmuyoruz)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# --- YENİ EKLENECEK GÜVENLİK BLOĞU ---
if not DEBUG:
    # 1. Tüm HTTP trafiğini otomatik olarak HTTPS'e yönlendirir
    SECURE_SSL_REDIRECT = True

    # 2. Oturum ve form güvenlik çerezlerinin sadece HTTPS üzerinden iletilmesini sağlar
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # 3. Tarayıcının XSS (Cross-Site Scripting) ve içerik türü manipülasyonu korumalarını açar
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # 4. Gunicorn/Nginx arkasında çalışırken Django'nun HTTPS trafiğini doğru algılamasını sağlar
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Virgülle ayrılmış hostları listeye çeviriyoruz
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'orders',
    'products',
    'branches',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kuraskuruyemis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kuraskuruyemis.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
        'CONN_MAX_AGE': 300,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'UTC'


USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CART_SESSION_ID = 'b2b_cart'


LOGIN_REDIRECT_URL = '/urunler/b2b-portal/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} [{module}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',  # Canlıda sadece INFO, WARNING, ERROR mesajlarını göster
            'propagate': True,
        },
        # Sipariş oluştururken (checkout vs.) oluşacak hataları yakalamak için
        'orders': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
