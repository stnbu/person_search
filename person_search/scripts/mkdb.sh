#!/bin/sh

PROJ="people_search"
USR="people_search"
# syncronize with django configuration:
PSWD="password"

# https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
cat <<EOF
CREATE DATABASE $PROJ;
CREATE USER $USR WITH PASSWORD '$PSWD';
ALTER ROLE $USR SET client_encoding TO 'utf8';
ALTER ROLE $USR SET default_transaction_isolation TO 'read committed';
ALTER ROLE $USR SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $PROJ TO $USR;
EOF

