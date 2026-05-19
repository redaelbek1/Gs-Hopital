from django.contrib import admin
from .models import Medecin


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite', 'service', 'disponible')
    list_filter = ('specialite', 'service', 'disponible')
    search_fields = ('user__nom', 'user__prenom', 'specialite')
