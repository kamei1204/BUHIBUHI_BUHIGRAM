"""
Django settings for BUHIBUHI_BUHIGRAM project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# トークンの有効時間を設定(python timeDelta)
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'di6)^h+y2$0vr3xu!g&v2m6g=g36c4=y%-)no_ce1p@@0a)pn+'

# SECURITY WARNING: don't run with debug turned on in production!
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

    'rest_framework',
    'djoser',
    # apiフォルダのappsのApiConfig(設定)を参照
    # アプリケーションを作った場合、必ずINSTALLED_APPSに追記
    'buhi_api.apps.BuhiApiConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# django rest_frameworkへアクセスを許可するため使用するURLをたす
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000"
]

ROOT_URLCONF = 'BUHIBUHI_BUHIGRAM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'BUHIBUHI_BUHIGRAM.wsgi.application'
# rest_framework 色々なオプションを設定できる
REST_FRAMEWORK = {
    # 特定のユーザーのみ閲覧できるようDEFAULT_PERMISSION_CLASSESを設定
    'DEFAULT_PERMISSION_CLASSES': [
        # ログインしているユーザーだけがviewを見れるようにする
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 認証の方法を設定　JWTAuthentication認証を指定
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # DEFAULT_PERMISSION_CLASSESおよびDEFAULT_AUTHENTICATION_CLASSESを設定すると、このプロジェクト内のviewにデフォルトで制限をかけることになる
    # 誰でも見れるviewを作る場合は、別途viewで設定する
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    # トークンの有効時間の設定　securityを高めることができる
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# djangoのdefaultに追加で設定した場合、必ず追記
AUTH_USER_MODEL = 'buhi_api.user'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# アバターの画像や投稿された画像をどのフォルダに入れるかを設定
# MEDIA_ROOTでBASE_DIR(プロジェクトの大本のフォルダ)の直下にmediaフォルダを作成してそこにデータを格納していく
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# mediaへのLINK
MEDIA_URL = '/media/'