from django.urls import path
from . import views

app_name = 'dossier_medical'

urlpatterns = [
    path('<int:pk>/', views.dossier_detail, name='detail'),
    path('<int:pk>/modifier/', views.dossier_update, name='update'),
    path('compte-rendu/nouveau/<int:rdv_id>/', views.compte_rendu_create, name='cr_create'),
    path('compte-rendu/<int:pk>/', views.compte_rendu_detail, name='cr_detail'),
]
