#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Compile translations"
python manage.py compilemessages

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Starting server"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
