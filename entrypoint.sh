# #!/bin/sh

# echo "🚀 Starting Django entrypoint..."

# echo "⏳ Waiting for PostgreSQL..."
# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 1
# done

# echo "✅ PostgreSQL is up!"

# python manage.py migrate --noinput
# python manage.py collectstatic --noinput

# exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
