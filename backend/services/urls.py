from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='list'),
    path('nouveau/', views.service_create, name='create'),
    path('<int:pk>/', views.service_detail, name='detail'),
    path('<int:pk>/modifier/', views.service_update, name='update'),
    path('<int:pk>/supprimer/', views.service_delete, name='delete'),
]
