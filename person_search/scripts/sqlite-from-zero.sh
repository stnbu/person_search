#!/bin/sh
# A helper script to re-set everything when using sqlite (think "make clean")

set -ue

read -p 'Blow away everything? [ENTER] for yes, CTRL-C to quit!' foo

rm -f /tmp/person_search.sqlite3
rm -rf person_search/migrations
python manage.py makemigrations person_search
python manage.py migrate
#python manage.py createsuperuser --username admin --noinput --email 'foo@example.com'
### This hack because we cannot set the password on the command line
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'password')" | python manage.py shell
