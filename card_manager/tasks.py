import datetime
from core.celery import app
from celery import shared_task

from .card_generator import CardGenerator
from .models import CardGeneration, Card


@shared_task()
def search_for_expired_cards():
    for item in Card.objects.filter(expired__lt=datetime.datetime.now(tz=None)):
        item.status = 'expired'
        item.save()


@app.task(bind=True)
def generate_cards(dict_id):
    CardGenerator().generate_cards(CardGeneration.objects.get(id=dict_id['id']))
