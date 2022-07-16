import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, View
from django.views.generic.edit import FormMixin

from .forms import SearchCardForm, GenerateCardForm
from .models import Card, CardGeneration
from .tasks import generate_cards
from .utilits import add_months_to_now


class CardList(FormMixin, ListView):
    model = Card
    template_name = 'card_list.html'  # noqa
    form_class = SearchCardForm
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        return Card.objects.all().order_by("issue_date", "id")


class CardSearch(CardList):
    def get_queryset(self):
        query = self.request.GET.dict()
        return Card.objects.filter(**self.get_serach_params(query))

    def get_serach_params(self, query):
        param_list = [
            {'param_name': 'BIN', 'rule': '{0}__icontains'},
            {'param_name': 'issue_date', 'rule': '{0}__icontains'},
            {'param_name': 'expired', 'rule': '{0}__icontains'},
            {'param_name': 'number', 'rule': '{0}__icontains'},
            {'param_name': 'status', 'rule': '{0}'},
        ]
        result = {}
        for param in param_list:
            value = query.get(param["param_name"])
            if value:
                result[param["rule"].format(param["param_name"])] = value
        return result

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


class DeleteCard(DeleteView):
    model = Card

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({'url': reverse_lazy('card_list')})


class ChangeStatusCard(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.card = None

    def post(self, request, *args, **kwargs):
        self.card = get_object_or_404(Card, pk=self.kwargs['pk'])
        self.update_card()
        self.card.save()
        return JsonResponse({'url': reverse_lazy('card_detail', kwargs={'pk': self.kwargs['pk']})})

    def update_card(self):
        raise Exception('You must overwrite this method')


class DeactivateCard(ChangeStatusCard):
    def update_card(self):
        self.card.status = 'not_activated'


class ActivateCard(ChangeStatusCard):
    def update_card(self):
        self.card.status = 'activated'
        self.card.issue_date = datetime.datetime.now(tz=None)
        self.card.expired = add_months_to_now(6)


class CardGenerator(FormMixin, ListView):
    model = CardGeneration
    template_name = 'card_generator.html'  # noqa
    form_class = GenerateCardForm
    success_url = reverse_lazy('card_generator')
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        return CardGeneration.objects.all().order_by("-created_at", "-id")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            card_generation = CardGeneration.objects.create(
                quantity=form.cleaned_data['quantity'],
                BIN=form.cleaned_data['BIN'],
                activity_expiration_date=form.cleaned_data['activity_expiration_date'],
            )
            generate_cards.delay({'id': card_generation.id})
            return self.form_valid(form)
        else:
            self.object_list = self.get_queryset()
            return self.form_invalid(form)
