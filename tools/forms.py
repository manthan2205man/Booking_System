from django import forms
from django.contrib.auth import get_user_model
from . models import *
from accounts.models import *


class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%Y/%m/%d '])

class DateInput(forms.DateInput):
    input_type = 'date'


class MapToolCreationForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['title', 'category', 'latitude', 'longitude', 'description', 'photo', 'price', 'address', 'city']
        widgets = {
            "latitude": forms.TextInput(attrs={'placeholder': 'Latitude', 'id': 'latitude', }),
            "longitude": forms.TextInput(attrs={'placeholder': 'Longitude', 'id': 'longitude', }),
        }


class BooknowCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['from_date', 'to_date']
        widgets = {'from_date': DateInput(),'to_date': DateInput()}


class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class MultiplePhotosForm(forms.ModelForm):

    photo1 = forms.ImageField(required=False)
    photo2 = forms.ImageField(required=False)
    photo3 = forms.ImageField(required=False)
    photo4 = forms.ImageField(required=False)

    class Meta:
        model = MultiplePhotos
        fields = ('photo1','photo2','photo3','photo4')
