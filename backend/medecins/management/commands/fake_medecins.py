from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import CustomUser
from medecins.models import Medecin
from services.models import Service

class Command(BaseCommand):
    help = 'Génère des médecins factices'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Nombre de médecins à créer')

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        count = kwargs['count']
        self.stdout.write(self.style.SUCCESS(f'Création de {count} médecins...'))
        
        services = list(Service.objects.all())
        if not services:
            self.stdout.write(self.style.ERROR("Aucun service n'existe. Veuillez d'abord exécuter 'fake_services'."))
            return

        specialites = ['Généraliste', 'Cardiologue', 'Neurologue', 'Pédiatre', 'Chirurgien', 'Oncologue']
        
        for _ in range(count):
            nom = fake.last_name()
            prenom = fake.first_name()
            email = f"dr_{fake.unique.email()}"
            user = CustomUser.objects.create_user(
                email=email,
                password='password123',
                nom=nom,
                prenom=prenom,
                role='medecin',
                telephone=fake.phone_number()
            )
            Medecin.objects.create(
                user=user,
                specialite=random.choice(specialites),
                service=random.choice(services),
                telephone=user.telephone
            )
            
        # Affectation de chefs de service
        for service in services:
            medecins_du_service = Medecin.objects.filter(service=service)
            if medecins_du_service.exists():
                service.chef_service = random.choice(medecins_du_service)
                service.save()
            
        self.stdout.write(self.style.SUCCESS(f'{count} médecins créés avec succès !'))
