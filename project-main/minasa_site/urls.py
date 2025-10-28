from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', core_views.login_view, name='login'),
    path('accounts/logout/', core_views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('quizzes/', include('quizzes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
