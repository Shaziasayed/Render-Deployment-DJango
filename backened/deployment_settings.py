from .settings import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['.onrender.com']

CSRF_TRUSTED_ORIGINS = ['https://render-deploy-react-code-pyy3.onrender.com']

STATIC_ROOT = BASE_DIR / 'staticfiles'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
