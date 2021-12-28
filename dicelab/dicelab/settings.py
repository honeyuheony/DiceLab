"""
Django settings for dicelab project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = ['13.125.28.69']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # News
    'news.apps.NewsConfig',
    # Professor
    'professor.apps.ProfessorConfig',
    # Member
    'member.apps.MemberConfig',
    # Course
    'course.apps.CourseConfig',
    # Project
    'project.apps.ProjectConfig',
    # Publication
    'publication.apps.PublicationConfig',
    # School
    'school.apps.SchoolConfig',
    # Seminar
    'seminar.apps.SeminarConfig',
    # Main
    'main.apps.MainConfig',
    # Demo
    'demo.apps.DemoConfig'
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

ROOT_URLCONF = 'dicelab.urls'

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

WSGI_APPLICATION = 'dicelab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'news', 'static'),
    os.path.join(BASE_DIR, 'professor', 'static'),
    os.path.join(BASE_DIR, 'member', 'static'),
    os.path.join(BASE_DIR, 'course', 'static'),
    os.path.join(BASE_DIR, 'project', 'static'),
    os.path.join(BASE_DIR, 'publication', 'static'),
    os.path.join(BASE_DIR, 'school', 'static'),
    os.path.join(BASE_DIR, 'seminar', 'static'),
    os.path.join(BASE_DIR, 'main', 'static'),
    os.path.join(BASE_DIR, 'demo', 'demo')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# Cache
CASHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Secret JSON 불러오기
SECRET_FILE = os.path.join(BASE_DIR, 'dicelab/secret.json')
with open(SECRET_FILE) as token:
    secrets = json.loads(token.read())

# Secret.json 데이터 가공


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {} Environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# Notion-Version 환경변수
NOTION_VERSION = '2021-08-16'
NEWS_DATABASE_ID = get_secret('news_Database_ID')
PAGE_ID = get_secret('Professor_Page_ID')
COURSE_DATABASE_ID = get_secret('course_database_ID')
SCHOOL_DATABASE_ID = get_secret('School_Database_ID')
MEMBER_GRADUATE_DATABASE_ID = get_secret('member_graduate_database_ID')
MEMBER_ALUMNI_DATABASE_ID = get_secret('member_alumni_database_ID')
PUBLICATION_DATABASE_ID = get_secret('Publication_Database_ID')
PATENTS_DATABASE_ID = get_secret('Patents_Database_ID')
PROJECTS_DATABASES_ID = get_secret('Projects_Database_ID')
AI_CHALLENGE_DATABASES_ID = get_secret('AI_Challenge_Database_ID')
SEMINAR_DATABASE_ID = get_secret('Seminar_Database_ID')
INTERNAL_INTEGRATION_TOKEN = get_secret('Internal_Integration_Token')

# celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'news_load': {
        'task': 'news.tasks.set_data',
        'schedule': crontab(minute=1, hour='*/1'),
        'args': ()
    },
    'course_load': {
        'task': 'course.tasks.set_data',
        'schedule': crontab(minute=3, hour='*/1'),
        'args': ()
    },
    'member_load': {
        'task': 'member.tasks.set_data',
        'schedule': crontab(minute=5, hour='*/1'),
        'args': ()
    },
    'professor_load': {
        'task': 'professor.tasks.set_data',
        'schedule': crontab(minute=7, hour='*/1'),
        'args': ()
    },
    'project_load': {
        'task': 'project.tasks.set_data',
        'schedule': crontab(minute=9, hour='*/1'),
        'args': ()
    },
    'publication_load': {
        'task': 'publication.tasks.set_data',
        'schedule': crontab(minute=11, hour='*/1'),
        'args': ()
    },
    'school_load': {
        'task': 'school.tasks.set_data',
        'schedule': crontab(minute=13, hour='*/1'),
        'args': ()
    },
    'seminar_load': {
        'task': 'seminar.tasks.set_data',
        'schedule': crontab(minute=15, hour='*/1'),
        'args': ()
    }
}
