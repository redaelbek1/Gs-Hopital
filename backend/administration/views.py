from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
import json
from rendezvous.models import RendezVous
from services.models import Service
from patients.models import Patient
from medecins.models import Medecin


@login_required
def dashboard_view(request):
    """Vue du tableau de bord administrateur."""
    if request.user.role != 'admin':
        return redirect('users:dashboard')

    context = {
        'total_patients': Patient.objects.count(),
        'total_medecins': Medecin.objects.count(),
        'total_rdv': RendezVous.objects.count(),
        'total_services': Service.objects.count(),
        'rdv_en_attente': RendezVous.objects.filter(statut='en_attente').count(),
        'rdv_confirmes': RendezVous.objects.filter(statut='confirme').count(),
        'rdv_termines': RendezVous.objects.filter(statut='termine').count(),
    }
    return render(request, 'administration/dashboard.html', context)


@login_required
def rapports_view(request):
    """Vue des rapports et statistiques."""
    if request.user.role != 'admin':
        return redirect('users:dashboard')

    # Consultations par mois (12 derniers mois)
    from django.utils import timezone
    from datetime import timedelta
    il_y_a_12_mois = timezone.now() - timedelta(days=365)

    rdv_par_mois = (
        RendezVous.objects
        .filter(statut='termine', date__gte=il_y_a_12_mois)
        .annotate(mois=TruncMonth('date'))
        .values('mois')
        .annotate(total=Count('id'))
        .order_by('mois')
    )

    labels_mois = [r['mois'].strftime('%b %Y') for r in rdv_par_mois]
    data_mois = [r['total'] for r in rdv_par_mois]

    # Services les plus actifs
    services_actifs = (
        Service.objects
        .annotate(nb_rdv=Count('medecins__rendezvous_medecin'))
        .order_by('-nb_rdv')[:8]
    )
    labels_services = [s.nom for s in services_actifs]
    data_services = [s.nb_rdv for s in services_actifs]

    # Médecins les plus actifs
    medecins_actifs = (
        Medecin.objects
        .annotate(nb_consultations=Count('rendezvous_medecin', filter=__import__('django.db.models', fromlist=['Q']).Q(rendezvous_medecin__statut='termine')))
        .order_by('-nb_consultations')[:8]
    )
    labels_medecins = [f"Dr {m.user.get_full_name()}" for m in medecins_actifs]
    data_medecins = [m.nb_consultations for m in medecins_actifs]

    context = {
        'labels_mois': json.dumps(labels_mois),
        'data_mois': json.dumps(data_mois),
        'labels_services': json.dumps(labels_services),
        'data_services': json.dumps(data_services),
        'labels_medecins': json.dumps(labels_medecins),
        'data_medecins': json.dumps(data_medecins),
        'total_consultations': RendezVous.objects.filter(statut='termine').count(),
        'service_top': services_actifs[0].nom if services_actifs else 'N/A',
        'medecin_top': f"Dr {medecins_actifs[0].user.get_full_name()}" if medecins_actifs else 'N/A',
    }
    return render(request, 'administration/rapports.html', context)
