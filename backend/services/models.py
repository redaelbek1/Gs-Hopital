from django.db import models


class Service(models.Model):
    """Modèle représentant un service hospitalier."""

    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    chef_service = models.ForeignKey(
        'medecins.Medecin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_dirige',
    )

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.nom

    def get_medecins(self):
        """Retourne la liste des médecins du service."""
        return self.medecins.all()
