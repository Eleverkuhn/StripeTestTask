#!/bin/sh

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

python manage.py migrate
python manage.py loaddata items.json
exec "$@"
