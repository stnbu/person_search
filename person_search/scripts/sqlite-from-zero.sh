#!/bin/sh

set -e

read -p 'Blow away everything? You sure?! [ENTER] for yes: ' foo

rm -f db.sqlite3
rm -rf person_search/migrations
python manage.py makemigrations person_search
python manage.py migrate
#python manage.py createsuperuser --username admin --noinput --email 'foo@example.com'
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell
### REALLY, DJANGO?
