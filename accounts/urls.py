
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.student_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/', views.student_profile, name='student_profile'),

    path('logout/', views.student_logout, name='logout'),
]
