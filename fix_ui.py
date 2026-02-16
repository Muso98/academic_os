import os

BASE_DIR = os.getcwd()
templates_dir = os.path.join(BASE_DIR, 'templates')
static_css_dir = os.path.join(BASE_DIR, 'static', 'css')

# Ensure directories exist
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_css_dir, exist_ok=True)

# 1. Write main_v5.css
css_content = """/* PREMIUM UI OVERHAUL v5 (Glass & Floating) - FORCED UPDATE */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

:root {
    --primary-color: #4f46e5;
    --primary-hover: #4338ca;
    --secondary-color: #64748b;
    --accent-color: #8b5cf6;
    --bg-body: #f1f5f9;
    --bg-surface: rgba(255, 255, 255, 0.9);
    --glass-border: 1px solid rgba(255, 255, 255, 0.2);
    --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    --sidebar-width: 260px;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-body);
    color: #1e293b;
    overflow-x: hidden;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

/* Floating Sidebar (Premium Gradient) */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: var(--sidebar-width);
    /* PREMIUM INDIGO GRADIENT */
    background: linear-gradient(180deg, #3730a3 0%, #1e1b4b 100%) !important;
    background-color: #1e1b4b !important; /* Fallback */
    color: #fff !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    padding: 1.5rem 1rem;
    overflow-y: auto;
}

.main-content {
    margin-left: var(--sidebar-width);
    padding: 2rem;
    min-height: 100vh;
    transition: all 0.3s ease;
}

.nav-link {
    color: #94a3b8;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    font-weight: 500;
    transition: all 0.2s ease;
}

.nav-link:hover {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.05);
    transform: translateX(2px);
}

.nav-link.active {
    background-color: var(--primary-color);
    color: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.nav-link i {
    font-size: 1.1rem;
    margin-right: 0.75rem;
    width: 20px;
    text-align: center;
    opacity: 0.9;
}

/* Cards */
.card {
    background: var(--bg-surface);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Profile */
.profile-cover {
    height: 180px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    border-radius: 1.5rem 1.5rem 0 0;
    position: relative;
    overflow: hidden;
}

.profile-avatar-container {
    margin-top: -75px;
    position: relative;
    z-index: 2;
}

.profile-avatar {
    width: 150px;
    height: 150px;
    border: 5px solid #fff;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    background: #fff;
}

/* Utilities */
.bg-indigo-subtle { background-color: #e0e7ff; }
.bg-success-subtle { background-color: #dcfce7; }
.bg-purple-subtle { background-color: #f3e8ff; }
.text-purple { color: #7e22ce; }
.hover-elevate:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
    .sidebar { transform: translateX(-110%); width: 80%; }
    .sidebar.show { transform: translateX(0); }
    .main-content { margin-left: 0; padding: 1rem; }
}
"""

with open(os.path.join(static_css_dir, 'main_v5.css'), 'w', encoding='utf-8') as f:
    f.write(css_content)

# 2. Write base.html
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Academic OS{% endblock %}</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% load static %}
    <!-- LINK TO NEW V5 CSS -->
    <link rel="stylesheet" href="{% static 'css/main_v5.css' %}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
</head>

<body class="bg-light">
    {% block layout %}
    <div class="d-flex">
        <!-- Sidebar -->
        <nav class="sidebar text-white">
            <a href="/" class="d-flex align-items-center mb-4 text-white text-decoration-none px-3">
                <span class="fs-4 fw-bold tracking-tight">Academic OS</span>
            </a>
            <ul class="nav nav-pills flex-column mb-auto">
                <li class="nav-item">
                    <a href="{% url 'dashboard' %}" class="nav-link {% if request.resolver_match.url_name == 'dashboard' %}active{% endif %}" aria-current="page">
                        <i class="bi bi-grid-1x2-fill"></i>
                        Dashboard
                    </a>
                </li>
                <li>
                    <a href="{% url 'task_list' %}" class="nav-link {% if 'tasks' in request.path %}active{% endif %}">
                        <i class="bi bi-check-square-fill"></i>
                        Tasks
                    </a>
                </li>
                <li>
                    <a href="{% url 'observation_list' %}" class="nav-link {% if 'observations' in request.path %}active{% endif %}">
                        <i class="bi bi-eye-fill"></i>
                        Observations
                    </a>
                </li>
                <li>
                    <a href="{% url 'resource_list' %}" class="nav-link {% if 'resources' in request.path %}active{% endif %}">
                        <i class="bi bi-folder-fill"></i>
                        Resources
                    </a>
                </li>
            </ul>
            <hr class="border-secondary opacity-25">
            <div class="dropdown px-3">
                <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown" aria-expanded="false">
                    <div class="rounded-circle bg-white text-primary d-flex align-items-center justify-content-center me-2 fw-bold" style="width: 32px; height: 32px;">
                        {{ request.user.username|slice:":1"|upper }}
                    </div>
                    <strong>{{ request.user.username }}</strong>
                </a>
                <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                    <li><a class="dropdown-item" href="{% url 'profile' %}">Profile</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li>
                        <form action="{% url 'logout' %}" method="post">
                            {% csrf_token %}
                            <button type="submit" class="dropdown-item">Sign out</button>
                        </form>
                    </li>
                </ul>
            </div>
        </nav>

        <!-- Main Content Wrapper -->
        <main class="main-content w-100">
            <div class="container-fluid">
                {% block header %}
                <header class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-4">
                    <h1 class="h3 fw-bold text-dark">{% block page_title %}Dashboard{% endblock %}</h1>
                </header>
                {% endblock %}

                {% block content %}
                {% endblock %}
            </div>
        </main>
    </div>
    {% endblock %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
"""

with open(os.path.join(templates_dir, 'base.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully created static/css/main_v5.css and updated templates/base.html")
