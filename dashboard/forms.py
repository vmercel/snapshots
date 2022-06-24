from django import forms
from .models import Data, Covid
#new
from random import randrange, uniform


class DataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ['country', 'user']


class LocationSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Data
        fields = ['latitude','longitude']


#new
import os
from pathlib import Path
# model_h5 = os.path.join(Machine, "covid_new_model1.h5")

class ImageForm(forms.ModelForm):
    class Meta:
        model = Covid
        fields = ['image']

