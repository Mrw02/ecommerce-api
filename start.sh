#!/bin/bash
python manage.py migrate --no-input
gunicorn ecomapi.wsgi --log-file -
