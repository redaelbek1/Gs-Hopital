from django import forms
from .models import DossierMedical


class DossierMedicalForm(forms.ModelForm):
    """Formulaire de mise à jour du dossier médical."""

    class Meta:
        model = DossierMedical
        fields = ('antecedents', 'allergies', 'groupe_sanguin')
        widgets = {
            'antecedents': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'groupe_sanguin': forms.TextInput(attrs={'class': 'form-control'}),
        }
