from django.urls import path
from . import views

urlpatterns = [
    path('committee/', views.committee_list, name='committee_list'),
    path('committee/settings/', views.committee_settings_update, name='committee_settings'),
    path('committee/add/', views.committee_create, name='committee_create'),
    path('committee/<int:pk>/edit/', views.committee_update, name='committee_update'),
    path('committee/<int:pk>/delete/', views.committee_delete, name='committee_delete'),
]
