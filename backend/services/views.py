from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service
from .forms import ServiceForm


@login_required
def service_list(request):
    """Liste des services hospitaliers."""
    services = Service.objects.select_related('chef_service__user').all()
    return render(request, 'services/list.html', {'services': services})


@login_required
def service_detail(request, pk):
    """Détail d'un service."""
    service = get_object_or_404(Service, pk=pk)
    medecins = service.medecins.select_related('user').all()
    return render(request, 'services/detail.html', {'service': service, 'medecins': medecins})


@login_required
def service_create(request):
    """Créer un nouveau service (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('services:list')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service créé avec succès.')
            return redirect('services:list')
    else:
        form = ServiceForm()

    return render(request, 'services/form.html', {'form': form, 'title': 'Nouveau Service'})


@login_required
def service_update(request, pk):
    """Modifier un service (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('services:list')

    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service modifié avec succès.')
            return redirect('services:detail', pk=pk)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'services/form.html', {'form': form, 'title': 'Modifier Service', 'service': service})


@login_required
def service_delete(request, pk):
    """Supprimer un service (admin uniquement)."""
    if request.user.role != 'admin':
        messages.error(request, "Accès non autorisé.")
        return redirect('services:list')

    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service supprimé avec succès.')
        return redirect('services:list')

    return render(request, 'services/delete.html', {'service': service})
