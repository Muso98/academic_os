import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from users.models import User
from organization.models import Organization
from .models import CertificateSequence

def is_hr_or_superuser(user):
    return user.is_superuser or getattr(user, 'is_hr_manager', False) or user.groups.filter(name='HR').exists()

@login_required
def print_employee_certificate(request, pk):
    # Get the target user
    employee = get_object_or_404(User, pk=pk)
    
    # Try to get the profile. Create a dummy or handle if none exists
    try:
        profile = employee.employee_profile
    except:
        profile = None

    # Get the dynamically auto-incrementing certificate number
    now = timezone.now()
    current_year = now.year
    cert_number = CertificateSequence.get_next_number(current_year)

    organization = Organization.objects.first()

    # Determine Exact Role
    ROLE_TRANSLATIONS = {
        'Director': 'direktori',
        'HeadOfDepartment': 'kafedra mudiri',
        'Teacher': "o'qituvchisi",
        'Admin': "tizim ma'muri",
        'Methodist': 'uslubchisi',
        'admin': 'tizim ma\'muri' # In case admin is lowercase
    }
    
    employee_position = "xodimi" # default
    if employee.groups.exists():
        group_name = employee.groups.first().name
        employee_position = ROLE_TRANSLATIONS.get(group_name, group_name.lower())
    elif profile and profile.qualification_category:
        employee_position = profile.qualification_category

    # Generate QR Code for Verification URL
    from django.urls import reverse
    verify_url = request.build_absolute_uri(reverse('verify_certificate', args=[employee.pk])) + f"?y={current_year}&n={cert_number}"
    qr_data = verify_url
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    context = {
        'employee': employee,
        'profile': profile,
        'organization': organization,
        'certificate_number': cert_number,
        'current_date': now,
        'employee_position': employee_position,
        'qr_code_base64': qr_code_base64,
    }
    return render(request, 'hr/certificate_print.html', context)

def verify_employee_certificate(request, pk):
    # Public view to verify certificate authenticity
    employee = get_object_or_404(User, pk=pk)
    
    try:
        profile = employee.employee_profile
    except:
        profile = None

    organization = Organization.objects.first()

    ROLE_TRANSLATIONS = {
        'Director': 'direktori',
        'HeadOfDepartment': 'kafedra mudiri',
        'Teacher': "o'qituvchisi",
        'Admin': "tizim ma'muri",
        'Methodist': 'uslubchisi',
        'admin': 'tizim ma\'muri'
    }
    
    employee_position = "xodimi"
    if employee.groups.exists():
        group_name = employee.groups.first().name
        employee_position = ROLE_TRANSLATIONS.get(group_name, group_name.lower())
    elif profile and profile.qualification_category:
        employee_position = profile.qualification_category
        
    cert_year = request.GET.get('y', timezone.now().year)
    cert_num = request.GET.get('n', 'Noma\'lum')

    context = {
        'employee': employee,
        'organization': organization,
        'employee_position': employee_position,
        'cert_year': cert_year,
        'cert_num': cert_num,
    }
    return render(request, 'hr/certificate_verify.html', context)
