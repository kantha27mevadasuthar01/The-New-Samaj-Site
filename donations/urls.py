from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_view, name='donate_view'),
    path('my-donations/', views.my_donations, name='my_donations'),
]
