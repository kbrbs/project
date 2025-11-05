from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:pk>/', views.game_detail, name='game_detail'),
    path('<int:pk>/submit/', views.submit_game, name='submit_game'),
    path('my-attempts/', views.my_attempts, name='my_attempts'),
]
