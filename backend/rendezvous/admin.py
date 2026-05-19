from django.contrib import admin
from .models import RendezVous


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'statut')
    list_filter = ('statut', 'date')
    search_fields = ('patient__user__nom', 'medecin__user__nom', 'motif')
    date_hierarchy = 'date'
