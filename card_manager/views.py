from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
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

        return Card.objects.filter(**new_query)

    def get_initial(self):
        return self.request.GET.dict()


class CardDetail(DetailView):
    model = Card
    template_name = 'card_details.html'  # noqa

    def get_object(self):
        return Card.objects.raw(
            '''SELECT card_manager_card.*, 
            card_manager_transaction.amount,
            card_manager_transaction.recipient, 
            card_manager_transaction.status as transaction_status,
            card_manager_transaction.date_created
            FROM card_manager_card
            LEFT JOIN card_manager_transaction 
            ON card_manager_transaction.card_id = card_manager_card.id
            WHERE card_manager_card.id = %s
            ORDER BY card_manager_transaction.date_created''',
            [self.kwargs['pk']]
        )


class DeleteCardView(DeleteView):
    model = Card

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        Transaction.objects.filter(card=obj).delete()
        obj.delete()
        return JsonResponse({'url': reverse_lazy('card_list')})

