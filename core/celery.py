from __future__ import absolute_import
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'search_for_expired_cards': {
        'task': 'card_manager.tasks.search_for_expired_cards',
        'schedule': 50.0
    },

}
