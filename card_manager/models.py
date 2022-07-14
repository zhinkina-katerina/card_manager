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
    number = models.CharField(max_length=10, validators=[check_for_invalid_characters])
    issue_date = models.DateTimeField(default=None)
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
    date_created = models.DateTimeField(auto_now=True)

class CardGeneration(models.Model):
    STRING_STATUS_CHOICES = (
        ('New', 'New'),
        ('In_process', 'In Process'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    ACTIVITY_EXPIRATION_DATE_CHOICES = (
        ("one_year", "1 year"),
        ("six_months", "6 months"),
        ("one_month", "1 month"),
    )
    status = models.CharField(max_length=20, default='New', choices=STRING_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    exception = models.TextField(default="")
    BIN = models.CharField(max_length=6, validators=[check_for_invalid_characters])
    activity_expiration_date = models.CharField(max_length=20, default='one_month', choices=ACTIVITY_EXPIRATION_DATE_CHOICES)