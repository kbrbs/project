from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('api/<int:pk>/', views.quiz_api_detail, name='quiz_api_detail'),
    path('submit/<int:pk>/', views.quiz_submit, name='quiz_submit'),
]
