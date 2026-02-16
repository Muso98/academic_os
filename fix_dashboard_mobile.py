import os

# Define path
base_dir = os.getcwd()
template_path = os.path.join(base_dir, 'templates', 'dashboard.html')

html_content = """{% extends "base.html" %}

{% block page_title %}Dashboard{% endblock %}

{% block header %}
<!-- Dashboard has its own greeting banner, so we hide the default header -->
<div class="pt-3"></div>
{% endblock %}

{% block content %}
<div class="row mb-4 animate-fade-in-up">
    <div class="col-12">
        <div class="card border-0 bg-primary text-white shadow-lg overflow-hidden position-relative">
            <div class="card-body p-4 p-md-5 position-relative" style="z-index: 2;">
                <h1 class="fw-bold mb-2 display-6 display-md-5">Welcome back, {{ user.first_name|default:user.username }}! 👋</h1>
                <p class="lead opacity-75 mb-0 fs-6 fs-md-5">Here's what's happening in your academic workspace today.</p>
            </div>
            <!-- Decorative Circle -->
            <div class="position-absolute end-0 top-0 translate-middle-y me-5 mt-5 rounded-circle bg-white"
                style="width: 300px; height: 300px; opacity: 0.1;"></div>
        </div>
    </div>
</div>

<div class="row g-4 mb-4 animate-fade-in-up" style="animation-delay: 0.1s;">
    <!-- Quick Stats -->
    <div class="col-md-6 col-lg-3">
        <div class="card h-100 border-0 shadow-sm hover-elevate">
            <div class="card-body">
                <div class="d-flex align-items-center mb-3">
                    <div class="rounded-circle bg-indigo-subtle p-3 text-primary me-3">
                        <i class="bi bi-trophy-fill fs-4"></i>
                    </div>
                    <div>
                        <h6 class="text-muted text-uppercase mb-1 small fw-bold">My KPI Score</h6>
                        <h2 class="mb-0 text-dark fw-bold">{{ kpi_score|default:"0" }}</h2>
                    </div>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-primary" role="progressbar" style="width: {{ kpi_score|default:'0' }}%"
                        aria-valuenow="{{ kpi_score }}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-6 col-lg-3">
        <div class="card h-100 border-0 shadow-sm hover-elevate">
            <div class="card-body">
                <div class="d-flex align-items-center mb-3">
                    <div class="rounded-circle bg-success-subtle p-3 text-success me-3">
                        <i class="bi bi-check-circle-fill fs-4"></i>
                    </div>
                    <div>
                        <h6 class="text-muted text-uppercase mb-1 small fw-bold">Completed Tasks</h6>
                        <h2 class="mb-0 text-dark fw-bold">{{ completed_tasks_count }}</h2>
                    </div>
                </div>
                <small class="text-success fw-medium"><i class="bi bi-arrow-up-short"></i> All time</small>
            </div>
        </div>
    </div>
</div>

<!-- Analytics Charts Row -->
<div class="row g-4 mb-4 animate-fade-in-up" style="animation-delay: 0.2s;">
    <div class="col-md-8">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
                <h5 class="card-title mb-0">Performance Analytics</h5>
            </div>
            <div class="card-body">
                <canvas id="performanceChart" height="120"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-header bg-white py-3">
                <h5 class="card-title mb-0">Task Distribution</h5>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center">
                <canvas id="taskChart" height="200"></canvas>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    <!-- Tasks Widget -->
    <div class="col-md-6">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-header bg-white py-3">
                <h5 class="card-title mb-0">Pending Tasks</h5>
            </div>
            <div class="card-body p-0">
                {% if pending_tasks %}
                <ul class="list-group list-group-flush">
                    {% for task in pending_tasks %}
                    <li class="list-group-item d-flex justify-content-between align-items-center px-4 py-3">
                        <div>
                            <h6 class="mb-0">{{ task.title }}</h6>
                            <small class="text-danger"><i class="bi bi-clock"></i> {{ task.deadline|date:"M d" }}</small>
                        </div>
                        <span class="badge bg-warning text-dark">{{ task.get_status_display|default:"Pending" }}</span>
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <p class="p-4 text-center text-muted mb-0">No pending tasks.</p>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Observations Widget -->
    <div class="col-md-6">
        <div class="card h-100 border-0 shadow-sm">
            <div class="card-header bg-white py-3">
                <h5 class="card-title mb-0">Recent Observations</h5>
            </div>
            <div class="card-body p-0">
                {% if recent_observations %}
                <ul class="list-group list-group-flush">
                    {% for obs in recent_observations %}
                    <li class="list-group-item d-flex justify-content-between align-items-center px-4 py-3">
                        <div>
                            <h6 class="mb-0">{{ obs.teacher.username }}</h6>
                            <small class="text-muted">{{ obs.date }} - {{ obs.topic }}</small>
                        </div>
                        <span class="badge bg-primary rounded-pill">{{ obs.total_score }} pts</span>
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <p class="p-4 text-center text-muted mb-0">No recent observations.</p>
                {% endif %}
                <div class="card-footer bg-white text-center py-2">
                    <a href="#" class="text-decoration-none small">View All</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        fetch("{% url 'dashboard_chart_data' %}")
            .then(response => response.json())
            .then(data => {
                // Task Distribution Chart (Doughnut)
                const taskCtx = document.getElementById('taskChart').getContext('2d');
                new Chart(taskCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.tasks.labels.length ? data.tasks.labels : ['No Tasks'],
                        datasets: [{
                            data: data.tasks.data.length ? data.tasks.data : [1],
                            backgroundColor: [
                                '#4338ca', // Primary
                                '#10b981', // Success
                                '#f59e0b', // Warning
                                '#64748b'  // Secondary
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { usePointStyle: true, font: { family: 'Inter' } }
                            }
                        }
                    }
                });

                // Performance Chart (Bar/Line)
                const perfCtx = document.getElementById('performanceChart').getContext('2d');
                new Chart(perfCtx, {
                    type: 'bar',
                    data: {
                        labels: data.observations.labels,
                        datasets: [{
                            label: 'Observation Scores',
                            data: data.observations.data,
                            backgroundColor: '#4338ca',
                            borderRadius: 6,
                            barThickness: 32
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 25, // Assuming max score around 20-25
                                grid: { color: '#f1f5f9' }
                            },
                            x: {
                                grid: { display: false }
                            }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            });
    });
</script>
{% endblock %}
"""

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully overwrote {template_path}")
