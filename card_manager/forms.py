from django.forms import ModelForm, widgets, TextInput

from .models import Card


class SearchCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchCardForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = Card
        fields = ('BIN', 'number', 'issue_date', 'expired', 'status')

        widgets = {
            'BIN': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'number': widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'issue_date': widgets.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'expired': widgets.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'status': widgets.Select(

                attrs={
                    'class': 'form-select',
                })
        }
        labels = {
            'BIN': 'BIN (series): first 6 digits of the card number'
        }
