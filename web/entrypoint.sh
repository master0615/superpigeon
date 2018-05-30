#!/usr/bin/env bash

python manage.py migrate \
&& gunicorn superpigeon.wsgi:application -w 2 -b :8001
