#!/bin/sh

python3 manage.py migrate


echo "Creating admin if not exist"
python manage.py create_admin \
--username "${ADMIN_USERNAME}" \
--password "${ADMIN_PASSWORD}" \
--email "${ADMIN_EMAIL}" \
--noinput \


python3 manage.py runserver 0.0.0.0:8000
