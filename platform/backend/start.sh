#!/bin/sh

python3 manage.py wait_for_db

if [ ${RESET_DB} = 1 ]
then
    python manage.py reset_db --noinput
fi

python3 manage.py makemigrations --noinput
python3 manage.py makemigrations api --noinput
python3 manage.py migrate --noinput

echo "Creating admin if not exist"
python3 manage.py create_admin \
--username "${ADMIN_USERNAME}" \
--password "${ADMIN_PASSWORD}" \
--email "${ADMIN_EMAIL}" \
--noinput \

# python3 manage.py collectstatic --noinput

# python3 manage.py review_db 

if [ ${DEBUG} = 0]
    python3 manage.py runserver 0.0.0.0:8000
then
    gunicorn backend.wsgi
fi
