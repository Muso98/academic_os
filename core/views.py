from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from workflow.models import Task
from academic.models import LessonObservation
from hr.models import KPIRecord
from django.db.models import Sum, Avg, Count
from .models import Notification
from hr.models import KPIRecord, Certificate

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    if notification.link:
        return redirect(notification.link)
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    user = request.user
    is_admin = user.is_superuser or user.is_staff
    
    recent_certificates = []

    if is_admin:
        # Global Stats for Admin
        # Average KPI across all users who have records
        kpi_score = KPIRecord.objects.aggregate(Avg('score_obtained'))['score_obtained__avg'] or 0
        kpi_score = round(kpi_score, 1) # Round for display
        
        # All pending tasks in the system
        pending_tasks = Task.objects.filter(status__in=['PENDING', 'IN_PROGRESS']).order_by('deadline')[:5]
        
        # Total completed tasks in system
        completed_tasks_count = Task.objects.filter(status='COMPLETED').count()
        
        # Recent observations (all teachers)
        recent_observations = LessonObservation.objects.all().order_by('-date')[:5]
        
        # Recent certificates (all users)
        recent_certificates = Certificate.objects.all().order_by('-date_issued')[:5]
        
    else:
        # Personal Stats
        kpi_score = KPIRecord.objects.filter(user=user).aggregate(Sum('score_obtained'))['score_obtained__sum'] or 0
        
        pending_tasks = Task.objects.filter(assignees=user, status__in=['PENDING', 'IN_PROGRESS']).order_by('deadline')[:5]
        completed_tasks_count = Task.objects.filter(assignees=user, status='COMPLETED').count()
        recent_observations = LessonObservation.objects.filter(teacher=user).order_by('-date')[:5]
        
        # Users don't see certificates on dashboard typically, but we can add:
        recent_certificates = Certificate.objects.filter(employee=user).order_by('-date_issued')[:5]

    context = {
        'kpi_score': kpi_score,
        'pending_tasks': pending_tasks,
        'completed_tasks_count': completed_tasks_count,
        'recent_observations': recent_observations,
        'recent_certificates': recent_certificates,
        'is_admin_view': is_admin,
    }
    return render(request, 'dashboard.html', context)

@login_required
def dashboard_chart_data(request):
    user = request.user
    is_admin = user.is_superuser or user.is_staff
    
    # Chart 1: Task Status Distribution
    task_status_data = []
    task_labels = []
    
    # Aggregate counts for each status
    for status, label in Task.STATUS_CHOICES:
        if is_admin:
            count = Task.objects.filter(status=status).count()
        else:
            count = Task.objects.filter(assignees=user, status=status).count()
            
        if count > 0:
            task_status_data.append(count)
            task_labels.append(label)

    # Chart 2: Recent Observation Scores
    if is_admin:
        # Admin sees strict chronological order of ALL observations
        observations = LessonObservation.objects.all().order_by('date')[:10]
    else:
        observations = LessonObservation.objects.filter(teacher=user).order_by('date')[:7]
        
    obs_dates = [obs.date.strftime('%Y-%m-%d') for obs in observations]
    obs_scores = [obs.total_score() for obs in observations]

    data = {
        'tasks': {
            'labels': task_labels,
            'data': task_status_data,
        },
        'observations': {
            'labels': obs_dates,
            'data': obs_scores,
        }
    }
    return JsonResponse(data)
