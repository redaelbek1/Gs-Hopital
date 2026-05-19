from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RendezVous
from .forms import RendezVousForm


def creer_notification(destinataire, message, lien=''):
    """Utilitaire pour créer une notification."""
    from users.models import Notification
    Notification.objects.create(
        destinataire=destinataire,
        message=message,
        lien=lien,
    )


@login_required
def rendezvous_list(request):
    """Liste des rendez-vous de l'utilisateur."""
    user = request.user
    if user.role == 'patient':
        rdvs = RendezVous.objects.filter(patient__user=user).select_related('medecin__user', 'patient__user')
    elif user.role == 'medecin':
        rdvs = RendezVous.objects.filter(medecin__user=user).select_related('medecin__user', 'patient__user')
    else:
        rdvs = RendezVous.objects.all().select_related('medecin__user', 'patient__user')

    return render(request, 'rendezvous/list.html', {'rendezvous': rdvs})


@login_required
def rendezvous_create(request):
    """Créer un nouveau rendez-vous (patient uniquement)."""
    if request.user.role != 'patient':
        messages.error(request, "Seul un patient peut prendre un rendez-vous.")
        return redirect('rendezvous:list')

    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.patient = request.user.patient_profile
            rdv.save()
            # Notifier le médecin
            creer_notification(
                destinataire=rdv.medecin.user,
                message=f"Nouveau rendez-vous demandé par {request.user.get_full_name()} "
                        f"le {rdv.date.strftime('%d/%m/%Y à %H:%M')}.",
                lien=f"/rendezvous/{rdv.pk}/",
            )
            messages.success(request, 'Rendez-vous créé avec succès. Le médecin va confirmer.')
            return redirect('rendezvous:list')
    else:
        form = RendezVousForm()

    return render(request, 'rendezvous/create.html', {'form': form})


@login_required
def rendezvous_detail(request, pk):
    """Détail d'un rendez-vous."""
    rdv = get_object_or_404(RendezVous.objects.select_related('medecin__user', 'patient__user'), pk=pk)
    return render(request, 'rendezvous/detail.html', {'rdv': rdv})


@login_required
def rendezvous_confirmer(request, pk):
    """Confirmer un rendez-vous (médecin uniquement)."""
    if request.user.role != 'medecin':
        messages.error(request, "Seul le médecin peut confirmer un rendez-vous.")
        return redirect('rendezvous:detail', pk=pk)

    rdv = get_object_or_404(RendezVous, pk=pk)
    rdv.confirmer()
    # Notifier le patient
    creer_notification(
        destinataire=rdv.patient.user,
        message=f"Votre rendez-vous du {rdv.date.strftime('%d/%m/%Y à %H:%M')} "
                f"avec le Dr {rdv.medecin.user.get_full_name()} a été confirmé.",
        lien=f"/rendezvous/{rdv.pk}/",
    )
    messages.success(request, 'Rendez-vous confirmé. Le patient a été notifié.')
    return redirect('rendezvous:detail', pk=pk)


@login_required
def rendezvous_refuser(request, pk):
    """Refuser un rendez-vous (médecin uniquement)."""
    if request.user.role != 'medecin':
        messages.error(request, "Seul le médecin peut refuser un rendez-vous.")
        return redirect('rendezvous:detail', pk=pk)

    rdv = get_object_or_404(RendezVous, pk=pk)
    rdv.annuler()
    # Notifier le patient
    creer_notification(
        destinataire=rdv.patient.user,
        message=f"Votre rendez-vous du {rdv.date.strftime('%d/%m/%Y à %H:%M')} "
                f"avec le Dr {rdv.medecin.user.get_full_name()} a été refusé. "
                f"Veuillez prendre un autre rendez-vous.",
        lien="/rendezvous/nouveau/",
    )
    messages.warning(request, 'Rendez-vous refusé. Le patient a été notifié.')
    return redirect('rendezvous:list')


@login_required
def rendezvous_annuler(request, pk):
    """Annuler un rendez-vous (patient ou médecin)."""
    rdv = get_object_or_404(RendezVous, pk=pk)
    rdv.annuler()
    messages.warning(request, 'Rendez-vous annulé.')
    return redirect('rendezvous:detail', pk=pk)
