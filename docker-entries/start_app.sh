#!/bin/sh

python manage.py migrate > /dev/null 2>&1
python manage.py runserver 0.0.0.0:$SERVER_PORT
