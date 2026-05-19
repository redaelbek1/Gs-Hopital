from django.db import models


class Ordonnance(models.Model):
    """Modèle représentant une ordonnance médicale."""

    id = models.BigAutoField(primary_key=True)
    rdv = models.ForeignKey(
        'rendezvous.RendezVous',
        on_delete=models.CASCADE,
        related_name='ordonnances',
    )
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    medecin = models.ForeignKey(
        'medecins.Medecin',
        on_delete=models.CASCADE,
        related_name='ordonnances',
    )


    class Meta:
        verbose_name = 'Ordonnance'
        verbose_name_plural = 'Ordonnances'
        ordering = ['-date']

    def __str__(self):
        return f"Ordonnance #{self.id} - {self.medecin} le {self.date.strftime('%d/%m/%Y')}"

    def telecharger_pdf(self):
        """Génère et retourne le PDF de l'ordonnance."""
        # TODO: Implémenter la génération PDF
        pass
