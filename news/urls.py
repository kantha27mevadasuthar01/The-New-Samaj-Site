from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.news_list, name='news_list'),
    path('add/', views.news_create, name='news_create'),
    path('edit/<int:pk>/', views.news_edit, name='news_edit'),
    path('delete/<int:pk>/', views.news_delete, name='news_delete'),
]
