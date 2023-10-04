"""
Django settings for api project.

Adapted from the auto-generated 'settings.py' by 
"django-admin startproject" using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os


from .base import *

ENVIRONMENT = os.environ.get("DJANGO_ENV", "development")
if ENVIRONMENT == "production":
    from .production import *
else:
    from .development import *
