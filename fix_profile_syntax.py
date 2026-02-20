import os

file_path = r'm:/my projects/ACADEMIC OS/academic_os/users/templates/users/profile.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '<!-- Certificates Section -->'
end_marker = '{% endblock %}'

good_section = """<!-- Certificates Section -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-3 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0"><i class="bi bi-award me-2 text-primary"></i>{% trans "Certificates & Awards" %}</h5>
                <a href="{% url 'certificate_create' %}" class="btn btn-primary btn-sm">
                    <i class="bi bi-plus-lg me-1"></i> {% trans "Add" %}
                </a>
            </div>
            <div class="card-body p-4">
                {% if certificates %}
                <div class="row g-3">
                    {% for cert in certificates %}
                    <div class="col-md-6">
                        <div class="card border {% if cert.is_expired %}border-danger{% else %}border-success{% endif %} h-100">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h6 class="fw-bold mb-0">{{ cert.name }}</h6>
                                    <form method="post" action="{% url 'certificate_delete' cert.id %}" class="d-inline">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-sm btn-outline-danger border-0" onclick="return confirm('Siz ushbu sertifikatni o\\'chirishni xohlaysizmi?')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </form>
                                </div>
                                {% if cert.issuer %}
                                <p class="text-muted small mb-2"><i class="bi bi-building me-1"></i>{{ cert.issuer }}</p>
                                {% endif %}
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <small class="text-muted d-block">{% trans "Issued:" %} {{ cert.date_issued|date:"d.m.Y" }}</small>
                                        {% if cert.expiry_date %}
                                        <small class="{% if cert.is_expired %}text-danger{% else %}text-success{% endif %} d-block">
                                            {% trans "Expires:" %} {{ cert.expiry_date|date:"d.m.Y" }}
                                            {% if cert.is_expired %}<i class="bi bi-exclamation-circle ms-1"></i>{% endif %}
                                        </small>
                                        {% endif %}
                                    </div>
                                    {% if cert.file %}
                                    <a href="{{ cert.file.url }}" class="btn btn-sm btn-outline-primary" download>
                                        <i class="bi bi-download"></i>
                                    </a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <div class="text-center py-5">
                    <i class="bi bi-award fs-1 text-muted mb-3"></i>
                    <p class="text-muted">{% trans "No certificates yet." %}</p>
                    <a href="{% url 'certificate_create' %}" class="btn btn-outline-primary">
                        <i class="bi bi-plus-lg me-2"></i>{% trans "Add first certificate" %}
                    </a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

if start_marker in content and end_marker in content:
    idx_start = content.find(start_marker)
    idx_end = content.rfind(end_marker) + len(end_marker) + 1
    new_content = content[:idx_start] + good_section
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Syntax success!')
else:
    print('Failed to find markers')
