import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.admin.sites import site
from django.contrib.admin.helpers import AdminForm
from users.models import User
from users.admin import UserAdmin

# Mock request
request = RequestFactory().get('/admin/users/user/add/')
request.user = User.objects.filter(is_superuser=True).first()

# Instantiate admin
ua = UserAdmin(User, site)

# Get the form class generated for add_view
FormClass = ua.get_form(request, obj=None)
print("Form fields:", FormClass().fields.keys())

# Create form instance
form_instance = FormClass()

# Get fieldsets
fieldsets = ua.get_fieldsets(request, obj=None)
print("Fieldsets:", fieldsets)

# Create admin form wrapper
admin_form = AdminForm(form_instance, fieldsets, {})

# Render fieldsets manually
output = []
for fieldset in admin_form:
    output.append(f"Fieldset: {fieldset.name}")
    for line in fieldset:
        for field in line:
            output.append(f"  Field: {field.field.name} | Widget: {field.field.field.widget}")

print("\n".join(output))
