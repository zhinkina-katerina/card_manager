from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, View
from django.views.generic.edit import FormMixin
import datetime

from .forms import SearchCardForm, GenerateCardForm
from .models import Card, Transaction, CardGeneration
from .tasks import generate_cards
from .card_generator import CardGenerator as CG

class CardList(FormMixin, ListView):
    model = Card
    template_name = 'card_list.html'  # noqa
    form_class = SearchCardForm
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Card.objects.all().order_by("issue_date", "id")


class CardSearch(CardList):
    def get_queryset(self):
        query = self.request.GET.dict()
        if query.get('page'):
            del query['page']
        if query.get('initial-issue_date'):
            del query['initial-issue_date']
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


class ChangeStatusCardView(View):

    def post(self, request, *args, **kwargs):
        card = get_object_or_404(Card, pk=self.kwargs['pk'])
        if card.status == 'activated':
            card.status = 'not_activated'
        elif card.status == 'not_activated' or card.status == 'expired':
            card.issue_date = datetime.datetime.now(tz=None)
            card.expired = CG().add_months(6)
            card.status = 'activated'
        card.save()
        return JsonResponse({'url': reverse_lazy('card_detail', kwargs={'pk': self.kwargs['pk']})})


class CardGenerator(FormMixin, ListView):
    model = CardGeneration
    template_name = 'card_generator.html'      # noqa
    form_class = GenerateCardForm
    success_url = reverse_lazy('card_generator')
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return CardGeneration.objects.all().order_by("-created_at", "-id")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            card_generation = CardGeneration.objects.create(
                quantity = form.cleaned_data['quantity'],
                BIN = form.cleaned_data['BIN'],
                activity_expiration_date = form.cleaned_data['activity_expiration_date'],
            )
            generate_cards.delay({'id': card_generation.id})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)