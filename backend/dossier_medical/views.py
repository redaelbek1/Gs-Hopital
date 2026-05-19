from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DossierMedical
from .forms import DossierMedicalForm
from django.utils import timezone


def check_dossier_access(user, dossier):
    """Vérifie si l'utilisateur a le droit d'accéder à ce dossier médical."""
    if user.role == 'admin':
        return True
    if user.role == 'patient' and dossier.patient.user == user:
        return True
    if user.role == 'medecin':
        # Le médecin doit avoir un rdv avec ce patient
        if dossier.patient.rendezvous_patient.filter(medecin=user.medecin_profile).exists():
            return True
    return False


@login_required
def dossier_detail(request, pk):
    """Détail du dossier médical."""
    dossier = get_object_or_404(DossierMedical.objects.select_related('patient__user'), pk=pk)
    
    if not check_dossier_access(request.user, dossier):
        messages.error(request, "Accès refusé. Vous n'avez pas l'autorisation de voir ce dossier.")
        return redirect('users:dashboard')
        
    return render(request, 'dossier_medical/detail.html', {'dossier': dossier})


@login_required
def dossier_update(request, pk):
    """Modifier le dossier médical."""
    dossier = get_object_or_404(DossierMedical, pk=pk)

    if not check_dossier_access(request.user, dossier) or request.user.role == 'patient':
        messages.error(request, "Accès refusé.")
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = DossierMedicalForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dossier médical mis à jour.')
            return redirect('dossier_medical:detail', pk=pk)
    else:
        form = DossierMedicalForm(instance=dossier)

    return render(request, 'dossier_medical/update.html', {'form': form, 'dossier': dossier})


@login_required
def ajouter_note_view(request, pk):
    """Ajoute une note rapide au dossier médical."""
    dossier = get_object_or_404(DossierMedical, pk=pk)
    
    if not check_dossier_access(request.user, dossier) or request.user.role not in ['medecin', 'admin']:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce dossier.")
        return redirect('dossier_medical:detail', pk=pk)

    if request.method == 'POST':
        note = request.POST.get('note', '').strip()
        if note:
            # On utilise la méthode de la classe DossierMedical comme demandé dans l'UML
            date_str = timezone.now().strftime("%d/%m/%Y %H:%M")
            signature = f"Dr. {request.user.get_full_name()}" if request.user.role == 'medecin' else "Admin"
            note_formatee = f"[{date_str} - {signature}] : {note}"
            dossier.ajouter_note(note_formatee)
            messages.success(request, "Note ajoutée avec succès au dossier.")
        else:
            messages.warning(request, "La note ne peut pas être vide.")
            
    return redirect('dossier_medical:detail', pk=pk)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DossierMedical, CompteRendu
from rendezvous.models import RendezVous


@login_required
def dossier_detail(request, pk):
    """Afficher le dossier médical d'un patient."""
    dossier = get_object_or_404(DossierMedical.objects.select_related('patient__user'), pk=pk)
    return render(request, 'dossier_medical/detail.html', {'dossier': dossier})


@login_required
def dossier_update(request, pk):
    """Mettre à jour le dossier médical."""
    from .forms import DossierMedicalForm
    dossier = get_object_or_404(DossierMedical, pk=pk)
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dossier mis à jour.')
            return redirect('dossier_medical:detail', pk=pk)
    else:
        form = DossierMedicalForm(instance=dossier)
    return render(request, 'dossier_medical/update.html', {'form': form, 'dossier': dossier})


@login_required
def compte_rendu_create(request, rdv_id):
    """Créer un compte-rendu pour un rendez-vous terminé (médecin uniquement)."""
    if request.user.role != 'medecin':
        messages.error(request, "Seul le médecin peut créer un compte-rendu.")
        return redirect('rendezvous:list')

    rdv = get_object_or_404(RendezVous, pk=rdv_id)

    if request.method == 'POST':
        cr = CompteRendu(
            rendezvous=rdv,
            medecin=request.user.medecin_profile,
            observations=request.POST.get('observations', ''),
            diagnostic=request.POST.get('diagnostic', ''),
            recommandations=request.POST.get('recommandations', ''),
        )
        cr.save()
        # Marquer le RDV comme terminé
        rdv.statut = 'termine'
        rdv.save()
        messages.success(request, 'Compte-rendu enregistré.')
        return redirect('rendezvous:detail', pk=rdv_id)

    return render(request, 'dossier_medical/compte_rendu_form.html', {'rdv': rdv})


@login_required
def compte_rendu_detail(request, pk):
    """Afficher un compte-rendu."""
    cr = get_object_or_404(CompteRendu.objects.select_related('rendezvous__patient__user', 'medecin__user'), pk=pk)
    return render(request, 'dossier_medical/compte_rendu_detail.html', {'cr': cr})
