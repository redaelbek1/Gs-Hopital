from django.core.management.base import BaseCommand
from faker import Faker
import random
import datetime
from rendezvous.models import RendezVous
from patients.models import Patient
from medecins.models import Medecin

class Command(BaseCommand):
    help = 'Génère des rendez-vous factices'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Nombre de rendez-vous à créer')

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        count = kwargs['count']
        
        patients = list(Patient.objects.all())
        medecins = list(Medecin.objects.all())
        
        if not patients or not medecins:
            self.stdout.write(self.style.ERROR("Il faut des patients et des médecins. Exécutez 'fake_patients' et 'fake_medecins' d'abord."))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Création de {count} rendez-vous...'))
        statuts = ['en_attente', 'confirme', 'annule', 'termine']
        
        for _ in range(count):
            patient = random.choice(patients)
            medecin = random.choice(medecins)
            date_rdv = fake.date_time_between(start_date="-1y", end_date="+1y", tzinfo=datetime.timezone.utc)
            
            RendezVous.objects.create(
                patient=patient,
                medecin=medecin,
                date=date_rdv,
                statut=random.choice(statuts),
                motif=fake.sentence()
            )
            
        self.stdout.write(self.style.SUCCESS(f'{count} rendez-vous créés avec succès !'))
