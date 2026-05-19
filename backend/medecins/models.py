from django.db import models
from django.conf import settings


class Medecin(models.Model):
    """Modèle représentant un médecin."""

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medecin_profile',
    )
    specialite = models.CharField(max_length=100)
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medecins',
    )
    telephone = models.CharField(max_length=20, blank=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Médecin'
        verbose_name_plural = 'Médecins'

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialite}"

    def get_planning(self):
        """Retourne la liste des rendez-vous du médecin."""
        return self.rendezvous_medecin.all().order_by('date')
