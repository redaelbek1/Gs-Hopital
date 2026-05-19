import os
import sys
import django

# Ajouter le dossier racine du projet au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from services.models import Service

# Liste des services de base à créer (sans le champ capacite qui n'existe pas dans votre modèle)
SERVICES_DE_BASE = [
    {
        'nom': 'Urgences',
        'description': 'Service d\'accueil pour les urgences médicales et chirurgicales 24h/24.'
    },
    {
        'nom': 'Cardiologie',
        'description': 'Service spécialisé dans les maladies du cœur et des vaisseaux.'
    },
    {
        'nom': 'Pédiatrie',
        'description': 'Service dédié aux soins médicaux des enfants et des nourrissons.'
    },
    {
        'nom': 'Neurologie',
        'description': 'Service traitant les maladies du système nerveux.'
    },
    {
        'nom': 'Chirurgie Générale',
        'description': 'Service dédié aux interventions chirurgicales diverses.'
    },
    {
        'nom': 'Maternité',
        'description': 'Service d\'obstétrique pour le suivi des grossesses et les accouchements.'
    },
    {
        'nom': 'Oncologie',
        'description': 'Service spécialisé dans le diagnostic et le traitement des cancers.'
    }
]

print("Création des services par défaut...")

crees = 0
for data in SERVICES_DE_BASE:
    service, created = Service.objects.get_or_create(
        nom=data['nom'],
        defaults={
            'description': data['description']
        }
    )
    if created:
        print(f"✅ Service créé : {data['nom']}")
        crees += 1
    else:
        print(f"ℹ️ Le service {data['nom']} existe déjà.")

print(f"\nTerminé ! {crees} nouveaux services ont été ajoutés à la base de données.")
