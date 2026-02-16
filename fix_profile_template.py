# Fix profile template
with open('users/templates/users/profile.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find certificates section
cert_start = None
for i, line in enumerate(lines):
    if '<!-- Certificates Section -->' in line:
        cert_start = i
        break

if cert_start:
    # Keep everything before certificates
    new_content = ''.join(lines[:cert_start])
    
    # Add fixed certificates section
    new_content += '''
<!-- Certificates Section -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-3 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0"><i class="bi bi-award me-2 text-primary"></i>Sertifikatlar va Mukofotlar</h5>
                <a href="{% url 'certificate_create' %}" class="btn btn-primary btn-sm">
                    <i class="bi bi-plus-lg me-1"></i> Qo'shish
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
                                        <button type="submit" class="btn btn-sm btn-outline-danger border-0" onclick="return confirm('Sertifikatni o\\'chirishga ishonchingiz komilmi?')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </form>
                                </div>
                                {% if cert.issuer %}
                                <p class="text-muted small mb-2"><i class="bi bi-building me-1"></i>{{ cert.issuer }}</p>
                                {% endif %}
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <small class="text-muted d-block">Berilgan: {{ cert.date_issued|date:"d.m.Y" }}</small>
                                        {% if cert.expiry_date %}
                                        <small class="{% if cert.is_expired %}text-danger{% else %}text-success{% endif %} d-block">
                                            Amal qiladi: {{ cert.expiry_date|date:"d.m.Y" }}
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
                    <p class="text-muted">Hozircha sertifikatlar yo'q.</p>
                    <a href="{% url 'certificate_create' %}" class="btn btn-outline-primary">
                        <i class="bi bi-plus-lg me-2"></i>Birinchi sertifikatni qo'shish
                    </a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    # Write back
    with open('users/templates/users/profile.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('✅ Template fixed successfully!')
else:
    print('❌ Certificates section not found')
