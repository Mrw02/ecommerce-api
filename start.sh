#!/bin/bash
python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn ecomapi.wsgi --log-file -
