from django.urls import path
from . import views

urlpatterns = [
    path('', views.directory, name='directory'),
    path('<int:pk>/', views.person_detail, name='person_detail'),
    path('manage/', views.manage_people, name='manage_people'),
    path('add/', views.add_person, name='add_person'),
    path('edit/<int:pk>/', views.edit_person, name='edit_person'),
    path('delete/<int:pk>/', views.delete_person, name='delete_person'),
]
