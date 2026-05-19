from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


SPECIALITES_CHOICES = [
    ('', '-- Choisir une spécialité --'),
    ('Cardiologie', 'Cardiologie'),
    ('Dermatologie', 'Dermatologie'),
    ('Endocrinologie', 'Endocrinologie'),
    ('Gastro-entérologie', 'Gastro-entérologie'),
    ('Généraliste', 'Médecine Générale'),
    ('Gynécologie', 'Gynécologie'),
    ('Neurologie', 'Neurologie'),
    ('Ophtalmologie', 'Ophtalmologie'),
    ('ORL', 'ORL'),
    ('Orthopédie', 'Orthopédie'),
    ('Pédiatrie', 'Pédiatrie'),
    ('Pneumologie', 'Pneumologie'),
    ('Psychiatrie', 'Psychiatrie'),
    ('Radiologie', 'Radiologie'),
    ('Rhumatologie', 'Rhumatologie'),
    ('Urologie', 'Urologie'),
    ('Chirurgie', 'Chirurgie'),
    ('Anesthésiologie', 'Anesthésiologie'),
    ('Autre', 'Autre'),
]


from services.models import Service
from patients.models import Patient

class CustomUserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription pour les utilisateurs."""

    specialite = forms.ChoiceField(
        choices=SPECIALITES_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_specialite'}),
        label='Spécialité',
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_service'}),
        label='Service',
        empty_label='-- Choisir un service --',
    )
    groupe_sanguin = forms.ChoiceField(
        choices=[('', '-- Choisir un groupe sanguin --')] + Patient.GROUPE_SANGUIN_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_groupe_sanguin'}),
        label='Groupe Sanguin',
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'nom', 'prenom', 'telephone', 'role', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        specialite = cleaned_data.get('specialite')
        service = cleaned_data.get('service')
        groupe_sanguin = cleaned_data.get('groupe_sanguin')

        if role == 'medecin':
            if not specialite:
                self.add_error('specialite', 'Veuillez choisir une spécialité.')
            if not service:
                self.add_error('service', 'Veuillez choisir un service.')
        
        if role == 'patient' and not groupe_sanguin:
            self.add_error('groupe_sanguin', 'Veuillez choisir votre groupe sanguin.')

        return cleaned_data


class LoginForm(forms.Form):
    """Formulaire de connexion."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour du profil."""

    class Meta:
        model = CustomUser
        fields = ('nom', 'prenom', 'telephone')
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
