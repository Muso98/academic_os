import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from users.models import User
from organization.models import Organization
from .models import CertificateSequence, SickLeave

def is_hr_or_superuser(user):
    return user.is_superuser or getattr(user, 'is_hr_manager', False) or user.groups.filter(name='HR').exists()

@login_required
def print_employee_certificate(request, pk):
    employee = get_object_or_404(User, pk=pk)
    try:
        profile = employee.employee_profile
    except:
        profile = None

    now = timezone.now()
    current_year = now.year
    cert_number = CertificateSequence.get_next_number(current_year)

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


# ---- Sick Leave Views ----

@login_required
def sick_leave_submit(request):
    """Xodim kasallik varaqasini yuklaydi."""
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        certificate_file = request.FILES.get('certificate_file')

        if not start_date or not end_date or not certificate_file:
            messages.error(request, "Barcha maydonlarni to'ldiring va faylni yuklang.")
        else:
            SickLeave.objects.create(
                employee=request.user,
                start_date=start_date,
                end_date=end_date,
                certificate_file=certificate_file,
            )
            messages.success(request, "Kasallik varaqangiz HR bo'limiga yuborildi. Kutib turing.")
            return redirect('sick_leave_list')

    return render(request, 'hr/sick_leave_submit.html')


@login_required
def sick_leave_list(request):
    """Xodim o'zining kasallik varaqalarini ko'radi."""
    leaves = SickLeave.objects.filter(employee=request.user).order_by('-submitted_at')
    return render(request, 'hr/sick_leave_list.html', {'leaves': leaves})


@login_required
@user_passes_test(is_hr_or_superuser)
def sick_leave_hr_list(request):
    """HR bo'limi barcha kasallik varaqalarini ko'radi."""
    status_filter = request.GET.get('status', '')
    leaves = SickLeave.objects.all().order_by('-submitted_at')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    return render(request, 'hr/sick_leave_hr_list.html', {
        'leaves': leaves,
        'status_filter': status_filter,
        'status_choices': SickLeave.STATUS_CHOICES,
    })


@login_required
@user_passes_test(is_hr_or_superuser)
def sick_leave_review(request, pk):
    """HR kasallik varaqasini tasdiqlaydi yoki rad etadi."""
    leave = get_object_or_404(SickLeave, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        hr_note = request.POST.get('hr_note', '')

        if action == 'approve':
            leave.status = SickLeave.STATUS_APPROVED
            msg = f"{leave.employee.get_full_name() or leave.employee.username} uchun {leave.days_count} kunlik kasallik tasdiqlandi."
            messages.success(request, msg)
        elif action == 'reject':
            leave.status = SickLeave.STATUS_REJECTED
            messages.warning(request, "Kasallik varaqasi rad etildi.")
        
        leave.hr_note = hr_note
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()
        leave.save()
        return redirect('sick_leave_hr_list')

    return render(request, 'hr/sick_leave_review.html', {'leave': leave})

