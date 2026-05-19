from django.db import models
from django.conf import settings


class Patient(models.Model):
    """Modèle représentant un patient."""

    GROUPE_SANGUIN_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
    )
    date_naissance = models.DateField()
    adresse = models.TextField(blank=True)
    groupe_sanguin = models.CharField(
        max_length=5,
        choices=GROUPE_SANGUIN_CHOICES,
        blank=True,
    )

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.user.get_full_name()

    def get_dossier(self):
        """Retourne le dossier médical du patient."""
        try:
            return self.dossier_medical
        except Exception:
            return None
