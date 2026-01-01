#!/bin/sh
python manage.py migrate
python manage.py loaddata items discounts taxes orders
exec "$@"
