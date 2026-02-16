from django.urls import path
from .views import (
    ObservationListView, ObservationCreateView, 
    ResourceListView, ResourceCreateView,
    methodist_dashboard, observation_journal
)

urlpatterns = [
    path('methodist/', methodist_dashboard, name='methodist_dashboard'),
    path('observations/', ObservationListView.as_view(), name='observation_list'),
    path('observations/journal/', observation_journal, name='observation_journal'),
    path('observations/new/', ObservationCreateView.as_view(), name='observation_create'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/new/', ResourceCreateView.as_view(), name='resource_create'),
]
