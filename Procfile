web: gunicorn card_manager.wsgi --log-file -
worker: celery -A core beat & celery -A core worker -l INFO
