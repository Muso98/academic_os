"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import dashboard_view, dashboard_chart_data, mark_notification_read
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/<uuid:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('dashboard/chart-data/', dashboard_chart_data, name='dashboard_chart_data'),
    path('', dashboard_view, name='dashboard'), # Root URL -> Dashboard
    path('tasks/', include('workflow.urls')), # Task Management
    path('academic/', include('academic.urls')), # Academic Monitoring
    path('users/', include('users.urls')), # User Profile
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('documents/', include('documents.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
