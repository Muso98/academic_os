from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db import transaction
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from academic.models import LessonObservation, ObservationCriteria, ObservationScore, Subject, EducationalResource

User = get_user_model()

# Helper function to check if user is Methodist
def is_methodist(user):
    return user.groups.filter(name='Methodist').exists() or user.is_superuser

# Methodist Dashboard
@user_passes_test(is_methodist)
def methodist_dashboard(request):
    """
    Dashboard for Methodist users showing:
    - Recent observations
    - Resource statistics
    - Teacher performance overview
    """
    recent_observations = LessonObservation.objects.select_related('teacher', 'observer', 'subject').order_by('-date')[:10]
    
    # Statistics
    total_observations = LessonObservation.objects.count()
    total_resources = EducationalResource.objects.count()
    
    # Teacher performance (average scores)
    teacher_stats = LessonObservation.objects.values('teacher__username', 'teacher__first_name', 'teacher__last_name').annotate(
        obs_count=Count('id'),
        avg_score=Avg('scores__score')
    ).order_by('-avg_score')[:5]
    
    context = {
        'recent_observations': recent_observations,
        'total_observations': total_observations,
        'total_resources': total_resources,
        'teacher_stats': teacher_stats,
    }
    
    return render(request, 'academic/methodist_dashboard.html', context)

# Observation Journal
@user_passes_test(is_methodist)
def observation_journal(request):
    """
    Mutual observation journal showing all observations with filters.
    """
    observations = LessonObservation.objects.select_related('teacher', 'observer', 'subject').order_by('-date')
    
    # Filters
    teacher_filter = request.GET.get('teacher')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if teacher_filter:
        observations = observations.filter(teacher_id=teacher_filter)
    
    if date_from:
        observations = observations.filter(date__gte=date_from)
    
    if date_to:
        observations = observations.filter(date__lte=date_to)
    
    # Get all teachers for filter dropdown
    teachers = User.objects.filter(observations_received__isnull=False).distinct()
    
    context = {
        'observations': observations,
        'teachers': teachers,
        'selected_teacher': teacher_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'academic/observation_journal.html', context)

class ObservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Teacher'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = LessonObservation
        fields = ['teacher', 'subject', 'date', 'topic', 'class_group']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'class_group': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ObservationListView(LoginRequiredMixin, ListView):
    model = LessonObservation
    template_name = 'academic/observation_list.html'
    context_object_name = 'observations'
    ordering = ['-date']

    def get_queryset(self):
        # Teachers see their own, others see all (simplified for now)
        if self.request.user.groups.filter(name='Teacher').exists():
            return LessonObservation.objects.filter(teacher=self.request.user)
        return LessonObservation.objects.all()

class ObservationCreateView(LoginRequiredMixin, CreateView):
    model = LessonObservation
    form_class = ObservationForm
    template_name = 'academic/observation_form.html'
    success_url = reverse_lazy('observation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['criteria'] = ObservationCriteria.objects.all()
        return context

    def form_valid(self, form):
        with transaction.atomic():
            # Save form without committing to database yet
            observation = form.save(commit=False)
            # Set the observer
            observation.observer = self.request.user
            # Now save to database
            observation.save()
            
            # Save scores
            criteria_ids = self.request.POST.getlist('criteria_id')
            for cid in criteria_ids:
                score_val = self.request.POST.get(f'score_{cid}')
                if score_val:
                    ObservationScore.objects.create(
                        observation=observation,
                        criteria_id=cid,
                        score=int(score_val)
                    )
        return redirect(self.success_url)

class ResourceListView(LoginRequiredMixin, ListView):
    model = EducationalResource
    template_name = 'academic/resource_list.html'
    context_object_name = 'resources'
    ordering = ['-created_at']

class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = EducationalResource
    fields = ['title', 'description', 'file', 'version']
    template_name = 'academic/resource_form.html'
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)
