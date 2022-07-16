web: gunicorn core.wsgi
worker: celery -A core beat & celery -A core worker -l INFO
