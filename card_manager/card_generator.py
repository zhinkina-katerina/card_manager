import calendar
import datetime
import random
import string

from .models import Card


class CardGenerator:
    def generate_cards(self, item):
        try:
            item.status = 'In Process'
            item.save()

            for _ in range(item.quantity):
                Card.objects.create(
                    BIN=item.BIN,
                    number=self.random_string_digits(10),
                    expired=self.get_expired_date(item.activity_expiration_date),
                    issue_date=datetime.datetime.now(tz=None),
                    cvv=self.random_string_digits(3),
                    balance=0.00,
                    status='activated'
                )
                item.status = 'Completed'
                item.save()
        except Exception as e:
            item.status = 'Failed'
            item.exception = str(e)
            item.save()

    def random_string_digits(self, length):
        return ''.join(random.choice(string.digits) for _ in range(length))

    def get_expired_date(self, instance):
        interval = {
            "one_year": 12,
            "six_months": 6,
            "one_month": 1,
        }[instance]
        return self.add_months(interval)

    def add_months(self, months):
        today = datetime.datetime.now(tz=None)
        month = today.month - 1 + months
        year = today.year + month // 12
        month = month % 12 + 1
        day = min(today.day, calendar.monthrange(year, month)[1])
        return datetime.datetime(year, month, day, hour=today.hour, minute=today.minute, second=today.second)
