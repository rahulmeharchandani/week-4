from django.urls import path
from . import views
from .views import register, login_view, logout_view, dashboard, password_reset_request

urlpatterns = [
    path('', login_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    
]
