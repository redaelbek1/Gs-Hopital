from django import forms
from .models import Medecin
from users.models import CustomUser


class MedecinForm(forms.ModelForm):
    """Formulaire de création/modification d'un médecin."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email du médecin'})
    )
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    prenom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        help_text='Laisser vide pour ne pas modifier (en édition).'
    )

    class Meta:
        model = Medecin
        fields = ('specialite', 'service', 'telephone', 'disponible')
        widgets = {
            'specialite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cardiologie'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '06 12 34 56 78'}),
            'disponible': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        self.instance_medecin = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if self.instance_medecin and self.instance_medecin.pk:
            self.fields['email'].initial = self.instance_medecin.user.email
            self.fields['nom'].initial = self.instance_medecin.user.nom
            self.fields['prenom'].initial = self.instance_medecin.user.prenom
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        medecin = super().save(commit=False)

        if medecin.pk:
            # Mise à jour
            user = medecin.user
            user.email = self.cleaned_data['email']
            user.nom = self.cleaned_data['nom']
            user.prenom = self.cleaned_data['prenom']
            if self.cleaned_data.get('password'):
                user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
                medecin.save()
        else:
            # Création
            user = CustomUser.objects.create_user(
                email=self.cleaned_data['email'],
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                password=self.cleaned_data['password'],
                role='medecin',
            )
            medecin.user = user
            if commit:
                medecin.save()

        return medecin
