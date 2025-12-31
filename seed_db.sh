# entrypoint.sh
#!/bin/sh
python manage.py migrate
python manage.py loaddata items.json
exec "$@"
