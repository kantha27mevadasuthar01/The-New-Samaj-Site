from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='accounts/change_password.html', success_url='/accounts/password-change-done/'), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
]
