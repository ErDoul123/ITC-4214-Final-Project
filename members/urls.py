from django.urls import path
from . import views


urlpatterns = [
    path('register_user', views.register_user, name='register_user'),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('profile_settings', views.profile_settings, name='profile_settings'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('users/', views.users_list, name='users_list'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('user/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]