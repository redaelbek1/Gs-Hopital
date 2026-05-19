from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('rapports/', views.rapports_view, name='rapports'),
]
