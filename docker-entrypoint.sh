#!/bin/bash
set -e

# Collect static files
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:${BACK_END_PORT:-8000}