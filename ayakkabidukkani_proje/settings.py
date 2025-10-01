"""
Django settings for ayakkabidukkani_proje project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-ixn&7gqnjc1m6hwsf!w4)9_0vd5&2w&76!0g^h7dati0i+9qqo'
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'katalog',
    'kullanici', 
    'crispy_forms', 
    'crispy_bootstrap5', 
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

ROOT_URLCONF = 'ayakkabidukkani_proje.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Bunlar Admin paneli ve hata denetimi için GEREKLİDİR!
                'django.template.context_processors.debug', 
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Bizim custom sepet sayacımız
                'katalog.context_processors.sepet_toplami'
            ],
        },
    },
]

WSGI_APPLICATION = 'ayakkabidukkani_proje.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
from pathlib import Path

# Media dosyalarının (Yüklenen resimler) diskte nerede saklanacağı
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Media dosyalarına tarayıcıdan erişmek için kullanılacak URL öneki
MEDIA_URL = '/media/'
# Başarılı girişten sonra kullanıcıyı yönlendireceği sayfa adı (URL name)
LOGIN_REDIRECT_URL = 'ayakkabi_listesi'  # Veya 'profil' view'ini yazınca 'profil' olur

# Kullanıcının giriş yapması gerektiğini söyleyeceğimiz sayfa adı
LOGIN_URL = 'login' 
LOGOUT_REDIRECT_URL = 'login'
 
# Bu ayarları dosyanın en altına ekleyin:
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"