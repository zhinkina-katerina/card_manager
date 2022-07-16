from django.contrib import admin

from .models import Transaction, Card, CardGeneration

admin.site.register(Transaction)
admin.site.register(Card)
admin.site.register(CardGeneration)
