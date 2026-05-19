from django.db import models


class RendezVous(models.Model):
    """Modèle représentant un rendez-vous médical."""

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]

    id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='rendezvous_patient',
    )
    medecin = models.ForeignKey(
        'medecins.Medecin',
        on_delete=models.CASCADE,
        related_name='rendezvous_medecin',
    )
    date = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
    )
    motif = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        ordering = ['-date']

    def __str__(self):
        return f"RDV - {self.patient} avec {self.medecin} le {self.date.strftime('%d/%m/%Y %H:%M')}"

    def confirmer(self):
        """Confirme le rendez-vous."""
        self.statut = 'confirme'
        self.save()

    def annuler(self):
        """Annule le rendez-vous."""
        self.statut = 'annule'
        self.save()
