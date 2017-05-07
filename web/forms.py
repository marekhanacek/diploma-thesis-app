from django import forms

from web.models import Offer, UserProfile
from web.service.language import change_language
from web.service.offer import create_feedback, create_offer
from web.service.user import save_user_location_to_session
from .models import Currency


class OfferSearchForm(forms.Form):
    amount_from = forms.CharField()
    amount_to = forms.CharField()
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

    def process(self, request):
        session = request.session
        amount_from = int(self.cleaned_data['amount_from'])
        amount_to = int(self.cleaned_data['amount_to'])
        currency_from = self.cleaned_data['currency_from'].id
        currency_to = self.cleaned_data['currency_to'].id
        input_offer = session['input_offer']

        input_offer['amount_from'] = amount_from
        input_offer['amount_to'] = amount_to

        if input_offer['currency_from'] != currency_from or input_offer['currency_to'] != currency_to:
            input_offer['amount_from'] = None
            input_offer['amount_to'] = None

        input_offer['currency_from'] = currency_from
        input_offer['currency_to'] = currency_to

        session.modified = True


class OfferForm(forms.Form):
    amount_from = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'style': 'width: 90px',
                'type': 'number'
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
    radius = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control map-radius-input',
                'placeholder': 'Enter searching radius',
                'type': 'number'
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

    def process(self, user):
        create_offer(
            lat=self.cleaned_data['lat'],
            lng=self.cleaned_data['lng'],
            radius=self.cleaned_data['radius'],
            amount=self.cleaned_data['amount_from'],
            comment=self.cleaned_data['comment'],
            currency_from=self.cleaned_data['currency_from'],
            currency_to=self.cleaned_data['currency_to'],
            user_created=user,
            address=self.cleaned_data['address'],
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

    def process(self, id, user):
        create_feedback(
            offer=Offer.objects.get(pk=id),
            user=user,
            comment=self.cleaned_data['comment'],
            stars=int(self.cleaned_data['stars']),
        )


class ChangePreferencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangePreferencesForm, self).__init__(*args, **kwargs)
        self.fields['language'].empty_label = None

    class Meta:
        model = UserProfile
        fields = [
            'home_currency',
            'exchange_currency',
            'language',
            'address',
            'radius',
            'phone',
            'lat',
            'lng',
            'basic_information'
        ]
        widgets = {
            'home_currency': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'exchange_currency': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'language': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control map-address-input', 'placeholder': 'Enter your address'}
            ),
            'radius': forms.TextInput(
                attrs={'class': 'form-control map-radius-input', 'placeholder': 'Enter searching radius'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}
            ),
            'lat': forms.HiddenInput(
                attrs={'class': 'map-lat'}
            ),
            'lng': forms.HiddenInput(
                attrs={'class': 'map-lng'}
            ),
            'basic_information': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter basic information about you'}
            )
        }

    def process(self, request):
        self.save()
        save_user_location_to_session(
            session=request.session,
            lat=float(self.cleaned_data['lat']),
            lng=float(self.cleaned_data['lng']),
            radius=float(self.cleaned_data['radius']),
            address=self.cleaned_data['address'],
        )
        change_language(request, self.cleaned_data['language'].identificator)
