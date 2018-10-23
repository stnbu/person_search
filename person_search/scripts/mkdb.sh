#!/bin/sh
# A helper script to re-set everything when using PostgreSQL
# (think "make clean")

set -ue

read -p 'Blow away everything? [ENTER] for yes, CTRL-C to quit!' foo

PERSON_SEARCH_RDBMS="POSTGRES"  # see person_search/settings.py
export PERSON_SEARCH_RDBMS

PROJ="person_search"
USER_RW="person_search"
# synchronize with django configuration:
PSWD="password"

sudo -u postgres psql <<EOF

DROP DATABASE $PROJ;
CREATE DATABASE $PROJ;

DROP USER IF EXISTS $USER_RW;
CREATE USER $USER_RW WITH PASSWORD '$PSWD';

ALTER ROLE $USER_RW SET client_encoding TO 'utf8';
ALTER ROLE $USER_RW SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE $PROJ TO $USER_RW;

EOF

rm -rf person_search/migrations
python manage.py makemigrations person_search
python manage.py migrate
#python manage.py createsuperuser --username admin --noinput --email 'foo@example.com'
### This hack because we cannot set the password on the command line
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'password')" | python manage.py shell
