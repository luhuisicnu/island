"""
Django settings for island project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import djcelery
djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q28=0)mjb!=vf74551(xl-vj75pm#qc-=^pzkvhl6xwe(p0x^9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'customize_auth',
    'qa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'customize_auth.login_management.AuthenticationMiddleware',
]

ROOT_URLCONF = 'island.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates/"],
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

WSGI_APPLICATION = 'island.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = BASE_DIR + '/media'
MEDIA_URL = '/media/'

# APPEND_SLASH = False

LOGIN_URL = '/auth/login/'
# 会话有效期为1天 (以秒计算)
SESSION_COOKIE_AGE = 86400

# celery
BROKER_URL = "redis://localhost/2"
BACKEND = 'redis://localhost/2'
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ENABLE_UTC = USE_TZ
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_RESULT_EXPIRES = 3600  # 任务结果的时效时间
# CELERYD_LOG_FILE = BASE_DIR + "/celery.log"  # log路径
# CELERYBEAT_LOG_FILE = BASE_DIR + "/beat.log"  # beat log路径
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']  # 允许的格式
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会死掉
CELERYD_TASK_TIME_LIMIT = 120    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 30}  # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行

# Auth Level
TOP_LEVEL_USER_LIMIT = 10
NEXT_LEVEL_USER_LIMIT = 100
OTHER_LEVEL_INTERGRAL_LIMIT = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
LEVEL_NAME = ['初学咋练', '初窥门径', '略有小成', '驾轻就熟', '融会贯通', '炉火纯青', '出类拔萃', '出神入化', '登峰造极', '返璞归真']


try:
    from .local import *
except ImportError:
    pass
