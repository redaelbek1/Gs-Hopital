from django.core.management.base import BaseCommand
from faker import Faker
from services.models import Service

class Command(BaseCommand):
    help = 'Génère des services factices'

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        self.stdout.write(self.style.SUCCESS('Création des services...'))
        services_noms = ['Cardiologie', 'Neurologie', 'Pédiatrie', 'Urgences', 'Chirurgie', 'Radiologie', 'Oncologie']
        count = 0
        for nom in services_noms:
            service, created = Service.objects.get_or_create(
                nom=nom,
                defaults={'description': fake.text(max_nb_chars=200)}
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} services créés avec succès !'))
