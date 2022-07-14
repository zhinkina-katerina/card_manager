from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import SearchCardForm
from .models import Card, Transaction


class CardList(FormMixin, ListView):
    model = Card
    template_name = 'card_list.html'  # noqa
    form_class = SearchCardForm
    paginate_by = 10

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


class CardDetail(DetailView):
    model = Card
    template_name = 'card_details.html'  # noqa

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs['pk']).prefetch_related(
            Prefetch('transaction_set', queryset=Transaction.objects.order_by('date_created'),
                     to_attr='transaction_order_by_date')).all()
