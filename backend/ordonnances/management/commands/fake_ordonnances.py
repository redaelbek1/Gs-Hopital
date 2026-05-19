from django.core.management.base import BaseCommand
from faker import Faker
import random
from ordonnances.models import Ordonnance
from rendezvous.models import RendezVous

class Command(BaseCommand):
    help = 'Génère des ordonnances factices'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=40, help='Nombre d\'ordonnances à créer')

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        count = kwargs['count']
        
        rendezvous = list(RendezVous.objects.filter(statut__in=['confirme', 'termine']))
        
        if not rendezvous:
            self.stdout.write(self.style.ERROR("Aucun rendez-vous confirmé ou terminé n'existe. Exécutez 'fake_rendezvous' d'abord."))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Création de {count} ordonnances...'))
        
        for _ in range(count):
            rdv = random.choice(rendezvous)
            Ordonnance.objects.create(
                rdv=rdv,
                medecin=rdv.medecin,
                contenu=fake.paragraph(nb_sentences=3)
            )
            
        self.stdout.write(self.style.SUCCESS(f'{count} ordonnances créées avec succès !'))
