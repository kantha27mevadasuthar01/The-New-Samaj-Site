from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('staff/', views.staff_portal, name='staff_portal'),
    path('staff/sub-admins/', views.manage_sub_admins, name='manage_sub_admins'),
    path('staff/sub-admins/create/', views.create_sub_admin, name='create_sub_admin'),
    path('staff/audit-logs/', views.view_audit_logs, name='view_audit_logs'),
    path('staff/members/', views.member_management, name='member_management'),
]
