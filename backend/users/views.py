from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomUserRegistrationForm, LoginForm, ProfileUpdateForm
from patients.models import Patient  # type: ignore
from medecins.models import Medecin  # type: ignore


def login_view(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.get_full_name()} !')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('users:login')


def register_view(request):
    """Vue d'inscription."""
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil selon le rôle
            if user.role == 'patient':
                Patient.objects.create(  # type: ignore
                    user=user,
                    date_naissance='2000-01-01',
                    groupe_sanguin=form.cleaned_data.get('groupe_sanguin', ''),
                )
            elif user.role == 'medecin':
                Medecin.objects.create(  # type: ignore
                    user=user,
                    specialite=form.cleaned_data.get('specialite', 'Généraliste'),
                    service=form.cleaned_data.get('service'),
                )
            messages.success(request, 'Compte créé avec succès ! Connectez-vous.')
            return redirect('users:login')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Vue du tableau de bord selon le rôle."""
    user = request.user
    context = {'user': user}

    if user.role == 'patient':
        try:
            patient = user.patient_profile
            context['patient'] = patient
            context['rendezvous'] = patient.rendezvous_patient.all()[:5]
            context['dossier'] = patient.get_dossier()
        except ObjectDoesNotExist:
            pass

    elif user.role == 'medecin':
        try:
            medecin = user.medecin_profile
            context['medecin'] = medecin
            context['rendezvous'] = medecin.rendezvous_medecin.filter(statut='en_attente')[:5]
            context['planning'] = medecin.get_planning()[:10]
        except ObjectDoesNotExist:
            pass

    elif user.role == 'admin':
        return redirect('administration:dashboard')

    return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    """Vue du profil utilisateur."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def notifications_view(request):
    """Liste des notifications de l'utilisateur."""
    notifications = request.user.notifications.all()
    # Marquer toutes comme lues à la visite
    notifications.filter(lue=False).update(lue=True)
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def marquer_lue(request, pk):
    """Marquer une notification comme lue."""
    from .models import Notification
    notif = Notification.objects.filter(pk=pk, destinataire=request.user).first()
    if notif:
        notif.lue = True
        notif.save()
    return redirect(notif.lien if notif and notif.lien else 'users:notifications')
