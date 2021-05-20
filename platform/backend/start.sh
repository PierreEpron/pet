#!/bin/sh

python3 manage.py wait_for_db
python manage.py reset_db --noinput

# python3 manage.py review_db 


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

python3 manage.py runserver 0.0.0.0:8000
