from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('festival-tour/', views.festival_tour, name='festival_tour'),
    path('profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/change-password/', views.change_password, name='change_password'),
]
