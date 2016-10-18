#!/usr/bin/env bash

./manage.py migrate
./manage.py load_metadata_fixtures
gunicorn flis_metadata.server.wsgi:application --bind 0.0.0.0:8000
