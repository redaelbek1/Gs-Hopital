from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient


@login_required
def patient_list(request):
    """Liste des patients avec recherche."""
    user = request.user

    if user.role == 'admin':
        patients = Patient.objects.select_related('user').all()
        # Recherche admin
        q = request.GET.get('q', '').strip()
        if q:
            patients = patients.filter(
                Q(user__nom__icontains=q) |
                Q(user__prenom__icontains=q) |
                Q(pk__icontains=q)
            )
    elif user.role == 'medecin':
        patients = Patient.objects.filter(
            rendezvous_patient__medecin=user.medecin_profile
        ).select_related('user').distinct()
        q = ''
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('users:dashboard')

    return render(request, 'patients/list.html', {'patients': patients, 'q': request.GET.get('q', '')})


@login_required
def patient_detail(request, pk):
    """Détail d'un patient."""
    patient = get_object_or_404(Patient.objects.select_related('user'), pk=pk)
    user = request.user

    autorise = False
    if user.role == 'admin':
        autorise = True
    elif user.role == 'patient' and patient.user == user:
        autorise = True
    elif user.role == 'medecin':
        if patient.rendezvous_patient.filter(medecin=user.medecin_profile).exists():
            autorise = True

    if not autorise:
        messages.error(request, "Vous n'êtes pas autorisé à consulter ce patient.")
        return redirect('users:dashboard')

    return render(request, 'patients/detail.html', {'patient': patient})
