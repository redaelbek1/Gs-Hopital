from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medecin
from .forms import MedecinForm


@login_required
def medecin_list(request):
    """Liste des médecins."""
    medecins = Medecin.objects.select_related('user', 'service').all()
    return render(request, 'medecins/list.html', {'medecins': medecins})


@login_required
def medecin_detail(request, pk):
    """Détail d'un médecin."""
    medecin = get_object_or_404(Medecin.objects.select_related('user', 'service'), pk=pk)
    rdvs = medecin.rendezvous_medecin.select_related('patient__user').order_by('-date')[:10]
    return render(request, 'medecins/detail.html', {'medecin': medecin, 'rdvs': rdvs})


@login_required
def medecin_create(request):
    """Créer un nouveau médecin (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('medecins:list')

    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médecin créé avec succès.')
            return redirect('medecins:list')
    else:
        form = MedecinForm()

    return render(request, 'medecins/form.html', {'form': form, 'title': 'Nouveau Médecin'})


@login_required
def medecin_update(request, pk):
    """Modifier un médecin (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('medecins:list')

    medecin = get_object_or_404(Medecin, pk=pk)
    if request.method == 'POST':
        form = MedecinForm(request.POST, instance=medecin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médecin modifié avec succès.')
            return redirect('medecins:detail', pk=pk)
    else:
        form = MedecinForm(instance=medecin)

    return render(request, 'medecins/form.html', {'form': form, 'title': 'Modifier Médecin', 'medecin': medecin})


@login_required
def medecin_delete(request, pk):
    """Supprimer un médecin (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('medecins:list')

    medecin = get_object_or_404(Medecin, pk=pk)
    if request.method == 'POST':
        user = medecin.user
        medecin.delete()
        user.delete()
        messages.success(request, 'Médecin supprimé avec succès.')
        return redirect('medecins:list')

    return render(request, 'medecins/delete.html', {'medecin': medecin})


@login_required
def medecin_planning(request, pk=None):
    """Vue planning calendrier du médecin."""
    import json
    from django.http import JsonResponse

    if pk:
        medecin = get_object_or_404(Medecin, pk=pk)
    else:
        if request.user.role != 'medecin':
            messages.error(request, "Accès non autorisé.")
            return redirect('users:dashboard')
        medecin = request.user.medecin_profile

    # Si requête AJAX pour récupérer les événements JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        rdvs = medecin.rendezvous_medecin.select_related('patient__user').all()
        events = []
        couleurs = {
            'en_attente': '#FFA500',
            'confirme': '#28a745',
            'annule': '#dc3545',
            'termine': '#6c757d',
        }
        for rdv in rdvs:
            events.append({
                'id': rdv.pk,
                'title': f"{rdv.patient.user.get_full_name()}",
                'start': rdv.date.isoformat(),
                'end': (rdv.date + __import__('datetime').timedelta(minutes=30)).isoformat(),
                'color': couleurs.get(rdv.statut, '#007bff'),
                'url': f'/rendezvous/{rdv.pk}/',
                'extendedProps': {
                    'statut': rdv.get_statut_display(),
                    'motif': rdv.motif,
                },
            })
        return JsonResponse(events, safe=False)

    return render(request, 'medecins/planning.html', {'medecin': medecin})
