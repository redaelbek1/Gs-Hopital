from django.contrib import admin
from .models import Ordonnance


@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'rdv', 'medecin', 'date')
    list_filter = ('date', 'medecin')
    search_fields = ('contenu', 'medecin__user__nom')
    readonly_fields = ('date',)
