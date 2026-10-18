from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from core.views import LoginView, LogoutView, LoginPageView, DashboardPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='api-login'),
    path('api/auth/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/core/', include('core.urls')),
    path('api/training/', include('training.urls')),
    
    # Modular Templates
    path('', DashboardPageView.as_view(template_name="dashboard.html"), name='home'),
    path('formations/', LoginPageView.as_view(template_name="training/formations.html"), name='formations'),
    path('inscriptions/', LoginPageView.as_view(template_name="training/inscriptions.html"), name='inscriptions'),
    path('documents/', LoginPageView.as_view(template_name="training/documents.html"), name='documents'),
    path('stats/', LoginPageView.as_view(template_name="training/stats.html"), name='stats'),
    path('users/', LoginPageView.as_view(template_name="training/users.html"), name='users'),
    path('login/', LoginPageView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
