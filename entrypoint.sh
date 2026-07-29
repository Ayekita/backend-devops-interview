#!/bin/sh
set -e

echo "Running migrations..."
uv run python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec uv run gunicorn core.wsgi:application --bind 0.0.0.0:8000