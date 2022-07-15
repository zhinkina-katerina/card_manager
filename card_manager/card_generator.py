import datetime
import random
import string

from .models import Card
from .utilits import add_months_to_now


class CardGenerator:
    def generate_cards(self, item):
        try:
            item.status = 'In Process'
            item.save()

            for _ in range(item.quantity):
                Card.objects.create(
                    BIN=item.BIN,
                    number=self.get_unique_card_number(item.BIN),
                    expired=self.get_expired_date(item.activity_expiration_date),
                    issue_date=datetime.datetime.now(tz=None),
                    cvv=self.random_string_digits(3),
                    balance=0.00,
                    status='activated'
                )
                item.status = 'Completed'
        except Exception as e:
            item.status = 'Failed'
            item.exception = str(e)
        finally:
            item.save()

    def random_string_digits(self, length):
        return ''.join(random.choice(string.digits) for _ in range(length))

    def get_expired_date(self, instance):
        interval = {
            "one_year": 12,
            "six_months": 6,
            "one_month": 1,
        }[instance]
        return add_months_to_now(interval)

    def get_unique_card_number(self, BIN):
        cards_whith_the_same_BIN = Card.objects.filter(BIN=BIN)
        exists_numbers = [f.number for f in cards_whith_the_same_BIN]
        card_number = self.random_string_digits(10)
        if card_number not in exists_numbers:
            return card_number
        if cards_whith_the_same_BIN:
            _ = 0
            while True:
                card_number = self.random_string_digits(10)
                if card_number not in exists_numbers:
                    return card_number
                if _ == 10:
                    raise Exception('Unable to create a valid number')
