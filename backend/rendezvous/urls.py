from django.urls import path
from . import views

app_name = 'rendezvous'

urlpatterns = [
    path('', views.rendezvous_list, name='list'),
    path('nouveau/', views.rendezvous_create, name='create'),
    path('<int:pk>/', views.rendezvous_detail, name='detail'),
    path('<int:pk>/confirmer/', views.rendezvous_confirmer, name='confirmer'),
    path('<int:pk>/refuser/', views.rendezvous_refuser, name='refuser'),
    path('<int:pk>/annuler/', views.rendezvous_annuler, name='annuler'),
]
