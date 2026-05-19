from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import RendezVous


class RendezVousForm(forms.ModelForm):
    """Formulaire de création de rendez-vous avec vérification de créneau."""

    class Meta:
        model = RendezVous
        fields = ('medecin', 'date', 'motif')
        widgets = {
            'medecin': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le motif de votre rendez-vous...',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        medecin = cleaned_data.get('medecin')
        date = cleaned_data.get('date')

        if medecin and date:
            # Vérifier que la date est dans le futur
            if date <= timezone.now():
                raise forms.ValidationError("La date du rendez-vous doit être dans le futur.")

            # Vérifier les chevauchements (créneau de 30 minutes)
            duree = timedelta(minutes=30)
            rdvs_existants = RendezVous.objects.filter(
                medecin=medecin,
                statut__in=['en_attente', 'confirme'],
            )
            # Exclure le RDV en cours de modification
            if self.instance and self.instance.pk:
                rdvs_existants = rdvs_existants.exclude(pk=self.instance.pk)

            for rdv in rdvs_existants:
                debut_existant = rdv.date
                fin_existant = rdv.date + duree
                debut_nouveau = date
                fin_nouveau = date + duree
                # Chevauchement si les créneaux se recoupent
                if debut_nouveau < fin_existant and fin_nouveau > debut_existant:
                    raise forms.ValidationError(
                        f"Ce créneau est déjà occupé. Le Dr {medecin} a un rendez-vous "
                        f"le {debut_existant.strftime('%d/%m/%Y à %H:%M')}. "
                        f"Veuillez choisir un autre horaire."
                    )
        return cleaned_data
