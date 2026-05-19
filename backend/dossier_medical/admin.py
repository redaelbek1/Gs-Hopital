from django.contrib import admin
from .models import DossierMedical


@admin.register(DossierMedical)
class DossierMedicalAdmin(admin.ModelAdmin):
    list_display = ('patient', 'groupe_sanguin', 'created_at')
    search_fields = ('patient__user__nom', 'patient__user__prenom')
    readonly_fields = ('created_at',)
