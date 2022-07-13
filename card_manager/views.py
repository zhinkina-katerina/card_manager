from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import SearchCardForm
from .models import Card


class CardList(FormMixin, ListView):
    model = Card
    template_name = 'card_list.html'
    form_class = SearchCardForm

    def get_queryset(self, *args, **kwargs):
        return Card.objects.all()


class CardSearch(CardList):
    def get_queryset(self):
        query = self.request.GET.dict()
        if query.get('page'):
            del query['page']
        new_query = {f'{x}__icontains': y for x, y in query.items() if y != ''}
        if new_query.get('status__icontains'):
            new_query['status'] = new_query['status__icontains']
            del new_query['status__icontains']
            print(new_query)

        return Card.objects.filter(**new_query)

    def get_initial(self):
        return self.request.GET.dict()
