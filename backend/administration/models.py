from django.db import models
from django.conf import settings


class Admin(models.Model):
    """Modèle représentant un administrateur hospitalier."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
    )
    niveau_acces = models.CharField(max_length=50)
    departement = models.CharField(max_length=100, blank=True)
    date_prise_poste = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'

    def __str__(self):
        return f"Admin - {self.user.get_full_name()}"

    def generer_rapport(self):
        """Génère un rapport administratif."""
        # TODO: Implémenter la génération de rapports
        pass

    def gerer_comptes(self):
        """Gère les comptes utilisateurs."""
        # TODO: Implémenter la gestion des comptes
        pass
