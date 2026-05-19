from django import forms
from .models import Ordonnance


class OrdonnanceForm(forms.ModelForm):
    """Formulaire de création d'ordonnance."""

    class Meta:
        model = Ordonnance
        fields = ('contenu',)
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Détaillez les prescriptions...',
            }),
        }
