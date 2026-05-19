from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_naissance', 'groupe_sanguin')
    list_filter = ('groupe_sanguin',)
    search_fields = ('user__nom', 'user__prenom', 'user__email')
