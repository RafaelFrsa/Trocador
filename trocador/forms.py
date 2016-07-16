from django import forms

from .models import Trocador

class TrocadorForm(forms.ModelForm):

    class Meta:
        model = Trocador
        fields = ('fluido1', 'fluido2','material',)