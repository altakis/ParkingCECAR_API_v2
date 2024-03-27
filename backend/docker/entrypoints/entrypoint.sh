#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py test

python -m manage runserver 0.0.0.0:8000

exec "$@"