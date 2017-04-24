from django import forms

from web.models import Language
from .models import Currency, UserProfile
from django.contrib.auth.models import User


class OfferSearchForm(forms.Form):
    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Insert amount',
                'style': 'width: 90px'
            }
        )
    )
    currency_from = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-left:-1px'
            }
        )
    )
    currency_to = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']


class OfferForm(forms.Form):
    amount_from = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'style': 'width: 90px'
            }
        )
    )
    amount_to = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 90px',
                'readonly': True
            }
        )
    )
    currency_from = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-left:-1px'
            }
        )
    )
    currency_to = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'style': 'margin-left:-1px'
            }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control map-address-input',
                'placeholder': 'Enter your address'
            }
        )
    )
    radius = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control map-radius-input',
                'placeholder': 'Enter searching radius'
            }
        )
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Enter comment to offer'
            }
        ),
        required=False
    )
    lat = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'map-lat',
            }
        ),
        required=False
    )
    lng = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'map-lng',
            }
        ),
        required=False
    )


class FeedbackForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Enter comment to offer'
            }
        ),
        required=True
    )
    stars = forms.CharField()


class ChangePreferencesForm(forms.Form):
    home_currency = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    exchange_currency = forms.ModelChoiceField(
        queryset=Currency.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control map-address-input',
                'placeholder': 'Enter your address'
            }
        )
    )
    radius = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control map-radius-input',
                'placeholder': 'Enter searching radius'
            }
        )
    )
    lat = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'map-lat',
            }
        ),
        required=False
    )
    lng = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'map-lng',
            }
        ),
        required=False
    )
    basic_information = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Enter basic information about you'
            }
        ),
        required=False
    )
