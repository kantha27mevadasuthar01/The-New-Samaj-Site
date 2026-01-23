from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_list, name='location_list'),
    path('manage/', views.manage_locations, name='manage_locations'),
    path('add/', views.add_location, name='add_location'),
    path('edit/<int:pk>/', views.edit_location, name='edit_location'),
    path('delete/<int:pk>/', views.delete_location, name='delete_location'),
]
