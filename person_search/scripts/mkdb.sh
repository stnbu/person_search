#!/bin/sh

read -p 'Blow away everything? [ENTER] for yes, CTRL-C to quit!' foo

PERSON_SEARCH_RDBMS="POSTGRES"  # see person_search/settings.py
export PERSON_SEARCH_RDBMS

PROJ="person_search"
USER_RW="person_search_rw"
USER_RO="person_search_ro"
# syncronize with django configuration:
PSWD="password"

sudo -u postgres psql <<EOF

DROP DATABASE $PROJ;
CREATE DATABASE $PROJ;

DROP USER IF EXISTS $USER_RW;
CREATE USER $USER_RW WITH PASSWORD '$PSWD';
DROP USER IF EXISTS $USER_RO;
CREATE USER $USER_RO WITH PASSWORD '$PSWD';

ALTER ROLE $USER_RW SET client_encoding TO 'utf8';
ALTER ROLE $USER_RW SET timezone TO 'UTC';
ALTER ROLE $USER_RO SET client_encoding TO 'utf8';
ALTER ROLE $USER_RO SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE $PROJ TO $USER_RW;

-- INPROD: Making "person_search_ro" a read-only user. It would be wise to audit the account in practice to make sure it cannot write anything RDBMS-wide.

GRANT CONNECT ON DATABASE $PROJ TO $USER_RO;
GRANT USAGE ON SCHEMA public TO $USER_RO;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO $USER_RO;

EOF

rm -rf person_search/migrations
python manage.py makemigrations person_search
python manage.py migrate
