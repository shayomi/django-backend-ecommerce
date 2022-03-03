from django import forms
from Art.models import Item
from django_countries.fields import CountryField, countries

COUNTRY_CHOICES = tuple(countries)
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class ItemForm(forms.ModelForm):

    class Meta():
        model = Item
        fields = ('title', 'item_image', 'price', 'description')

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
    country  = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True)
    zip = forms.CharField()
    same_shipping_address = forms.BooleanField(widget = forms.CheckboxInput())
    save_info = forms.BooleanField(widget = forms.CheckboxInput())
    payment_options = forms.ChoiceField(widget = forms.RadioSelect, choices = PAYMENT_CHOICES)
