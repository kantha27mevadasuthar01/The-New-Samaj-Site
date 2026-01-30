from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Specific Sub-Admin Login URL as requested
    path('Sub-Admin/loge in/', views.sub_admin_login_view, name='sub_admin_login'),
]
