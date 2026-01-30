from django.urls import path
from . import views

urlpatterns = [
    path('', views.directory, name='people_directory'),
    path('<int:pk>/', views.person_detail, name='person_detail'),
    path('add/', views.add_person, name='add_person'),
    path('edit/<int:pk>/', views.edit_person, name='edit_person'),
    path('delete/<int:pk>/', views.delete_person, name='delete_person'),
    path('add-to-committee/<int:person_pk>/', views.add_to_committee, name='add_to_committee'),
    path('download/', views.download_directory, name='download_directory'),
]
