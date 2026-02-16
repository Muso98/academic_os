from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<uuid:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<uuid:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
]
