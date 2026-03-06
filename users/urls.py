from django.urls import path
from .views import (profile_view, certificate_create, certificate_delete,
                    user_management, user_create, user_edit, user_delete)

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('certificates/add/', certificate_create, name='certificate_create'),
    path('certificates/<uuid:certificate_id>/delete/', certificate_delete, name='certificate_delete'),
    # User Management (superadmin only)
    path('manage/', user_management, name='user_management'),
    path('manage/add/', user_create, name='user_create'),
    path('manage/<uuid:user_id>/edit/', user_edit, name='user_edit'),
    path('manage/<uuid:user_id>/delete/', user_delete, name='user_delete'),
]
