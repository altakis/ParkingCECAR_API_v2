import os

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / "subdir".
from .constants import BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Internal Apps and Middleware config
from .app_def import *
# Database connection config
from .db_def import *
# Authorization, Internationalization and Static folders
from .auth_int_static_def import *
# Primarily external Apps configuration
from .misc_def import *

from .logging import *
