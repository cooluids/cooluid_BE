from pathlib import Path

#my import
import os, json
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent

secret_files = os.path.join(BASE_DIR, ".secrets", ".secrets.json")

with open(secret_files) as f:
    secrets = json.loads(f.read())

def get_sercret(value, secrets = secrets):
    try:
        return secrets[value]
    except KeyError:
        error_msg = "Set the {} environment variable".format(value)
        raise ImproperlyConfigured(error_msg)
    
SECRET_KEY = get_sercret("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    # my apps
    'User',
    'rest_framework',
    # 'rest_framework_jwt',

]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#         # 다른 인증 클래스들 추가 가능
#     ),
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    
]

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000',
#     'http://localhost:8000',
# )

ROOT_URLCONF = 'cooluid_BE.urls'

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

WSGI_APPLICATION = 'cooluid_BE.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_AGE = 60 * 60 * 3
SESSION_SAVE_EVERY_REQUEST = True  
SESSION_COOKIE_DOMAIN = "localhost"
SESSION_COOKIE_SECURE = False



from google.oauth2 import service_account

gcs_secret_path = os.path.join(BASE_DIR, ".secrets", ".storage_service.json")

with open(gcs_secret_path) as f:
    gcs_secrets = json.loads(f.read())

def get_gcs_secret(value, secret=gcs_secrets):
    try:
        return secret[value]
    except KeyError:
        error_msg = "{} 설정을 확인해주세요".format(value)
        raise ImproperlyConfigured(error_msg)


DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = get_gcs_secret("GS_BUCKET_NAME")
GS_PROJECT_ID = get_gcs_secret("project_id")


GS_AUTO_CREATE_BUCKET = True

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    gcs_secret_path
)

MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)