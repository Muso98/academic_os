import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
from users.models import User
from organization.models import Organization
from .models import CertificateSequence, SickLeave

def link_callback(uri, rel):
    import os
    from django.conf import settings
    # Handle static paths like '/static/fonts/...' or 'static/fonts/...'
    if uri.startswith('/static/'):
        path = os.path.join(str(settings.BASE_DIR), uri.lstrip('/'))
    elif uri.startswith('static/'):
        path = os.path.join(str(settings.BASE_DIR), uri)
    else:
        path = uri
        
    if os.path.isfile(path):
        return path
    return uri

# Monkeypatch xhtml2pdf to fix font loading on Windows (NamedTemporaryFile lock issue)
import xhtml2pdf.files
def windows_safe_get_named_tmp_file(self):
    import os
    path = str(self.uri)
    if path.startswith('file:///'):
        path = path[8:]
    if os.path.isfile(path):
        class FakeTmp:
            def __init__(self, name):
                self.name = name
            def write(self, data): pass
            def flush(self): pass
            def close(self): pass
        return FakeTmp(path)
    
    import tempfile
    data = self.get_data()
    tmp_file = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False)
    if data:
        tmp_file.write(data)
        tmp_file.flush()
    tmp_file.close()
    
    class FakeTmp2:
        def __init__(self, name):
            self.name = name
        def write(self, data): pass
        def flush(self): pass
        def close(self):
            try:
                os.unlink(self.name)
            except:
                pass
    return FakeTmp2(tmp_file.name)

xhtml2pdf.files.BaseFile.get_named_tmp_file = windows_safe_get_named_tmp_file

ROLE_TRANSLATIONS = {
    'Director': _('direktori'),
    'HeadOfDepartment': _('kafedra mudiri'),
    'Teacher': _("o'qituvchisi"),
    'Admin': _("tizim ma'muri"),
    'Methodist': _('uslubchisi'),
    'admin': _("tizim ma'muri")
}

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
    
    employee_position = _("xodimi")
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

@login_required
def download_my_certificate_pdf(request):
    employee = request.user
    try:
        profile = employee.employee_profile
    except:
        profile = None

    now = timezone.now()
    current_year = now.year
    cert_number = CertificateSequence.get_next_number(current_year)

    organization = Organization.objects.first()
    
    employee_position = _("xodimi")
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
        'is_pdf': True,
        'fonts_dir': os.path.join(settings.BASE_DIR, 'static', 'fonts').replace('\\', '/'),
    }
    
    template = get_template('hr/certificate_print.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="malumotnoma_{employee.username}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('PDF yaratishda xatolik yuz berdi.', status=500)
    
    return response

def verify_employee_certificate(request, pk):
    employee = get_object_or_404(User, pk=pk)
    
    try:
        profile = employee.employee_profile
    except:
        profile = None

    organization = Organization.objects.first()
    
    employee_position = _("xodimi")
    if employee.groups.exists():
        group_name = employee.groups.first().name
        employee_position = ROLE_TRANSLATIONS.get(group_name, group_name.lower())
    elif profile and profile.qualification_category:
        employee_position = profile.qualification_category
        
    cert_year = request.GET.get('y', timezone.now().year)
    cert_num = request.GET.get('n', _('Noma\'lum'))

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
            messages.error(request, _("Barcha maydonlarni to'ldiring va faylni yuklang."))
        else:
            SickLeave.objects.create(
                employee=request.user,
                start_date=start_date,
                end_date=end_date,
                certificate_file=certificate_file,
            )
            messages.success(request, _("Kasallik varaqangiz HR bo'limiga yuborildi. Kutib turing."))
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
            messages.warning(request, _("Kasallik varaqasi rad etildi."))
        
        leave.hr_note = hr_note
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()
        leave.save()
        return redirect('sick_leave_hr_list')

    return render(request, 'hr/sick_leave_review.html', {'leave': leave})

