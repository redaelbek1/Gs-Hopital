from django.db import models


class DossierMedical(models.Model):
    """Modèle représentant le dossier médical d'un patient."""

    id = models.BigAutoField(primary_key=True)
    patient = models.OneToOneField(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='dossier_medical',
    )
    antecedents = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dossier Médical'
        verbose_name_plural = 'Dossiers Médicaux'

    def __str__(self):
        return f"Dossier de {self.patient}"

    def ajouter_note(self, note):
        """Ajoute une note aux antécédents du dossier."""
        if self.antecedents:
            self.antecedents += f"\n---\n{note}"
        else:
            self.antecedents = note
        self.save()


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='patients.Patient')
def create_dossier_medical(sender, instance, created, **kwargs):
    """Crée automatiquement un dossier médical lorsqu'un patient est créé."""
    if created:
        DossierMedical.objects.create(
            patient=instance,
            groupe_sanguin=instance.groupe_sanguin
        )
    else:
        # Synchroniser le groupe sanguin si le patient est mis à jour
        if hasattr(instance, 'dossier_medical') and instance.dossier_medical.groupe_sanguin != instance.groupe_sanguin:
            instance.dossier_medical.groupe_sanguin = instance.groupe_sanguin
            instance.dossier_medical.save()



class CompteRendu(models.Model):
    """Compte-rendu de consultation rédigé par le médecin."""
    rendezvous = models.OneToOneField(
        'rendezvous.RendezVous',
        on_delete=models.CASCADE,
        related_name='compte_rendu',
    )
    medecin = models.ForeignKey(
        'medecins.Medecin',
        on_delete=models.CASCADE,
        related_name='comptes_rendus',
    )
    observations = models.TextField(blank=True)
    diagnostic = models.TextField(blank=True)
    recommandations = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Compte-rendu'
        verbose_name_plural = 'Comptes-rendus'
        ordering = ['-date']

    def __str__(self):
        return f"Compte-rendu RDV #{self.rendezvous_id} - {self.date.strftime('%d/%m/%Y')}"
