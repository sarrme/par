from django import forms
from .models import Simulation, ChoixActif
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
class ChoixForm(forms.ModelForm):
    class Meta:
        model= Simulation
        exclude=['imagefirst','imagesecond',]
    def clean(self):
        cleaned_data = super().clean()
        date_debut=cleaned_data.get('date_debut')
        date_fin=cleaned_data.get('date_fin')
        if date_debut==None or date_fin==None:
            raise ValidationError(_('Date erreur - Vérifier que la date est de la forme 2018-12-30'))
        elif date_debut>datetime.date.today():
            raise ValidationError(_('Date erreur - la date de début doit au maximum hier'))
        elif date_fin< date_debut+ datetime.timedelta(days=365):
            raise ValidationError(_('Date erreur - Vous devez depasser 1 ans pour le choix des dates'))
        else: 
            return cleaned_data
