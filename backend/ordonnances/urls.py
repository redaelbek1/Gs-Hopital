from django.urls import path
from . import views

app_name = 'ordonnances'

urlpatterns = [
    path('', views.ordonnance_list, name='list'),
    path('nouvelle/<int:rdv_id>/', views.ordonnance_create, name='create'),
    path('<int:pk>/', views.ordonnance_detail, name='detail'),
    path('<int:pk>/pdf/', views.ordonnance_pdf, name='pdf'),
]
