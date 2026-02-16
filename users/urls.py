from django.urls import path
from .views import profile_view, certificate_create, certificate_delete

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('certificates/add/', certificate_create, name='certificate_create'),
    path('certificates/<uuid:certificate_id>/delete/', certificate_delete, name='certificate_delete'),
]
