from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import CustomUser
from patients.models import Patient

class Command(BaseCommand):
    help = 'Génère des patients factices'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='Nombre de patients à créer')

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        count = kwargs['count']
        self.stdout.write(self.style.SUCCESS(f'Création de {count} patients...'))
        
        groupes_sanguins = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for _ in range(count):
            nom = fake.last_name()
            prenom = fake.first_name()
            email = fake.unique.email()
            user = CustomUser.objects.create_user(
                email=email,
                password='password123',
                nom=nom,
                prenom=prenom,
                role='patient',
                telephone=fake.phone_number()
            )
            Patient.objects.create(
                user=user,
                date_naissance=fake.date_of_birth(minimum_age=1, maximum_age=90),
                adresse=fake.address(),
                groupe_sanguin=random.choice(groupes_sanguins)
            )
            
        self.stdout.write(self.style.SUCCESS(f'{count} patients créés avec succès !'))
