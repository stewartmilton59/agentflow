from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),

    # User Management
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<uuid:pk>/', views.user_detail_view, name='user_detail'),
    path('users/<uuid:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<uuid:pk>/delete/', views.user_delete_view, name='user_delete'),

    # Activity Logs
    path('activity-log/', views.activity_log_view, name='activity_log'),
]