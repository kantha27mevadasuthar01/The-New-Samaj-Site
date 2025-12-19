from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('photos/', views.photos, name='photos'),
    path('videos/', views.videos, name='videos'),

    # Members
    path('manage-members/', views.manage_members, name='manage_members'),
    path('add-member/', views.add_member, name='add_member'),
    path('edit-member/<int:id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:id>/', views.delete_member, name='delete_member'),
    path('members/', views.members, name='members'),  

    # Posts
    path('add-post/', views.add_post, name='add_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

    # Home editor
    path('edit-home/', views.edit_home, name='edit_home'),

    # Authentication
    path('login/', views.EditorLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
