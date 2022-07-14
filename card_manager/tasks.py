from celery import shared_task

from .card_generator import CardGenerator
from .models import CardGeneration, Card
import datetime

@shared_task()
def search_for_expired_cards():
    for item in Card.objects.filter(expired__lt=datetime.datetime.now(tz=None)):
        item.status = 'expired'
        item.save()

@shared_task()
def generate_cards(dict_pk):
    CardGenerator().generate_cards(CardGeneration.objects.get(id = dict_pk['id']))
