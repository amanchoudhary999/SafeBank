from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('confirm-password/<str:next_action>/', views.confirm_password, name='confirm_password'),
    path('deposit/', views.deposit, name='deposit'),  # Add actual view
    path('withdraw/', views.withdraw, name='withdraw'),  # Add actual view
    path('transfer/', views.transfer, name='transfer'),  # Add actual view
    path('history/', views.transaction_history, name='transaction_history'),
    path('confirm-password/', views.confirm_password, name='confirm_password'),
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-transactions/', views.admin_transactions, name='admin_transactions'),
]
