from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    """Formulaire de création/modification d'un service."""

    class Meta:
        model = Service
        fields = ('nom', 'description', 'chef_service')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du service'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description du service...'}),
            'chef_service': forms.Select(attrs={'class': 'form-control'}),
        }
