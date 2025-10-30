from django.urls import path
from . import views
from .admin_panel import views as admin_views

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
    # Custom admin panel
    path('admin-panel/', admin_views.DashboardView.as_view(), name='admin_dashboard'),
    path('admin-panel/sections/', admin_views.SectionListView.as_view(), name='admin_sections'),
    path('admin-panel/sections/add/', admin_views.SectionCreateView.as_view(), name='admin_section_add'),
    path('admin-panel/sections/<int:pk>/edit/', admin_views.SectionUpdateView.as_view(), name='admin_section_edit'),
    path('admin-panel/sections/<int:pk>/delete/', admin_views.SectionDeleteView.as_view(), name='admin_section_delete'),

    path('admin-panel/media/', admin_views.MediaListView.as_view(), name='admin_media'),
    path('admin-panel/media/add/', admin_views.MediaCreateView.as_view(), name='admin_media_add'),
    path('admin-panel/media/<int:pk>/edit/', admin_views.MediaUpdateView.as_view(), name='admin_media_edit'),
    path('admin-panel/media/<int:pk>/delete/', admin_views.MediaDeleteView.as_view(), name='admin_media_delete'),

    path('admin-panel/moderation/', admin_views.ModerationListView.as_view(), name='admin_moderation'),
    path('admin-panel/moderation/<int:pk>/update/', admin_views.moderation_update, name='admin_moderation_update'),
    path('admin-panel/download/<int:pk>/', admin_views.download_media, name='admin_media_download'),
    path('admin-panel/visits.json', admin_views.visits_json, name='admin_visits_json'),
    path('admin-panel/top-pages.json', admin_views.top_pages_json, name='admin_top_pages_json'),
    path('admin-panel/export/visits.csv', admin_views.export_visits_csv, name='admin_export_visits'),
    path('admin-panel/export/moderation.csv', admin_views.export_moderation_csv, name='admin_export_moderation'),

    # Quizzes CRUD
    path('admin-panel/quizzes/', admin_views.QuizListView.as_view(), name='admin_quizzes'),
    path('admin-panel/quizzes/add/', admin_views.QuizCreateView.as_view(), name='admin_quiz_add'),
    path('admin-panel/quizzes/<int:pk>/edit/', admin_views.QuizUpdateView.as_view(), name='admin_quiz_edit'),
    path('admin-panel/quizzes/<int:pk>/delete/', admin_views.QuizDeleteView.as_view(), name='admin_quiz_delete'),
    # Users
    path('admin-panel/users/', admin_views.UserListView.as_view(), name='admin_users'),
    path('admin-panel/users/add/', admin_views.UserCreateView.as_view(), name='admin_user_add'),
    path('admin-panel/users/<int:pk>/edit/', admin_views.UserUpdateView.as_view(), name='admin_user_edit'),
    path('admin-panel/users/<int:pk>/delete/', admin_views.UserDeleteView.as_view(), name='admin_user_delete'),
]
