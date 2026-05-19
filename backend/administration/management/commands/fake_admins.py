from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import CustomUser
from administration.models import Admin

class Command(BaseCommand):
    help = 'Génère des administrateurs factices'

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        self.stdout.write(self.style.SUCCESS('Création des administrateurs...'))
        count = 0
        for i in range(2):
            nom = fake.last_name()
            prenom = fake.first_name()
            email = f"admin_{fake.unique.email()}"
            user = CustomUser.objects.create_user(
                email=email,
                password='password123',
                nom=nom,
                prenom=prenom,
                role='admin',
                telephone=fake.phone_number()
            )
            Admin.objects.create(
                user=user,
                niveau_acces=random.choice(['Super', 'Standard']),
                departement='Direction'
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} administrateurs créés avec succès !'))
