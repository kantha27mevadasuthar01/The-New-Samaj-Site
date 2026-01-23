from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('manage/', views.manage_gallery, name='manage_gallery'),
    path('add/', views.add_media, name='add_media'),
    path('edit/<int:pk>/', views.edit_media, name='edit_media'),
    path('delete/<int:pk>/', views.delete_media, name='delete_media'),
]
