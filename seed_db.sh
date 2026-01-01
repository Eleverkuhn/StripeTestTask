#!/bin/sh
python manage.py migrate
python manage.py loaddata items discounts taxes orders
PYTHONPATH=./payments python create_admin.py
exec "$@"
