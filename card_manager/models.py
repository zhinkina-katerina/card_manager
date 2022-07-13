from django.core.exceptions import ValidationError
from django.db import models


def check_for_invalid_characters(value):
    if value.isdigit() == False:
        raise ValidationError('This field can only contain numbers')


class Card(models.Model):
    STRING_STATUS_CHOICES = (
        ('activated', 'Activated'),
        ('not_activated', 'Not activated'),
        ('expired', 'Expired'),
    )

    BIN = models.CharField(max_length=6, validators=[check_for_invalid_characters])  # Bank Identification Number
    number = models.CharField(max_length=8, validators=[check_for_invalid_characters])
    issue_date = models.DateTimeField()
    expired = models.DateTimeField()
    cvv = models.CharField(max_length=3, validators=[check_for_invalid_characters])
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=13, choices=STRING_STATUS_CHOICES, blank=True)


class Transaction(models.Model):
    STRING_STATUS_CHOICES = (
        ('new', 'New'),
        ('in_process', 'In process'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STRING_STATUS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
