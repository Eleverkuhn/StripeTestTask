#!/bin/sh
python manage.py migrate
python manage.py loaddata items discounts taxes orders
python manage.py collectstatic --noinput
PYTHONPATH=./payments python create_admin.py
exec "$@"
