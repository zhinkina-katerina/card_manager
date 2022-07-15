web: python manage.py runserver 0.0.0.0:$PORT
worker: celery -A core beat & celery -A core worker -l INFO
