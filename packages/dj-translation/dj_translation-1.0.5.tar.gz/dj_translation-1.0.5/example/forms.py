from django import forms

from example.models import TranslatableModel


class TranslatableForm(forms.ModelForm):
    class Meta:
        model = TranslatableModel
        fields = '__all__'
