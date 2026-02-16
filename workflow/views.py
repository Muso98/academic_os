from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        required=False
    )
    # Custom field for dependencies
    dependency_tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        required=False,
        label="Dependencies"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'deadline', 'assignees']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate initial dependencies
            self.fields['dependency_tasks'].initial = [
                dep.depends_on for dep in self.instance.dependencies.all()
            ]
            # Exclude self from options to prevent confusion (validation exists in model too)
            self.fields['dependency_tasks'].queryset = Task.objects.exclude(pk=self.instance.pk)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m() # Save assignees
            
            # Save dependencies
            current_dependencies = set(self.cleaned_data['dependency_tasks'])
            # Clear existing simple way (or smart update)
            # For simplicity: delete all types where task=instance and recreate
            from .models import TaskDependency
            instance.dependencies.all().delete()
            for task in current_dependencies:
                TaskDependency.objects.create(task=instance, depends_on=task)
                
        return instance

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'workflow/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Users see tasks assigned to them OR created by them
        return Task.objects.filter(assignees=self.request.user) | Task.objects.filter(creator=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'workflow/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'workflow/task_detail.html'
    context_object_name = 'task'

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'workflow/task_form.html'
    success_url = reverse_lazy('task_list')
