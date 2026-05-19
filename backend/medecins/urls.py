from django.urls import path
from . import views

app_name = 'medecins'

urlpatterns = [
    path('', views.medecin_list, name='list'),
    path('nouveau/', views.medecin_create, name='create'),
    path('planning/', views.medecin_planning, name='planning'),
    path('<int:pk>/', views.medecin_detail, name='detail'),
    path('<int:pk>/modifier/', views.medecin_update, name='update'),
    path('<int:pk>/supprimer/', views.medecin_delete, name='delete'),
    path('<int:pk>/planning/', views.medecin_planning, name='planning_pk'),
]
