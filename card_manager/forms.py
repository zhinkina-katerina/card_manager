from django import forms
from django.core.validators import MinLengthValidator

from .models import Card, CardGeneration, check_for_invalid_characters, check_for_negative_numbers_and_zero


class SearchCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SearchCardForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = Card
        fields = ('BIN', 'number', 'issue_date', 'expired', 'status')

        widgets = {
            'BIN': forms.widgets.TextInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'number': forms.widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'issue_date': forms.widgets.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }),
            'expired': forms.widgets.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
            'status': forms.widgets.Select(

                attrs={
                    'class': 'form-select',
                })
        }
        labels = {
            'BIN': 'BIN (series): first 6 digits of the card number'
        }


class GenerateCardForm(forms.Form):
    BIN = forms.CharField(
        label='BIN (series): first 6 digits of the card number',
        max_length=6,
        validators=[check_for_invalid_characters, MinLengthValidator(6)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }))
    activity_expiration_date = forms.CharField(
        widget=forms.Select(
            choices=CardGeneration.ACTIVITY_EXPIRATION_DATE_CHOICES,
            attrs={
                'class': "btn btn-primary dropdown-toggle d-block",
                'data-toggle': 'dropdown',
                'type': 'button'},
        ))
    quantity = forms.IntegerField(
        max_value=1000,
        validators=[check_for_negative_numbers_and_zero],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
