#!/bin/bash

python manage.py collectstatic
cp -r /app/static/. web/static
cp -r /app/static_front/. web/static

python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model();
User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | python manage.py shell

gunicorn --bind 0.0.0.0:8000 tracker.wsgi