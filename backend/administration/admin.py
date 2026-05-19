from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'niveau_acces', 'departement', 'date_prise_poste')
    list_filter = ('niveau_acces', 'departement')
    search_fields = ('user__nom', 'user__prenom')
