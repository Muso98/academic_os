from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm, ProfileUpdateForm
from hr.models import EmployeeProfile, Certificate

User = get_user_model()

SCHOOL_ROLES = [
    ('Director', "Direktor"),
    ('DeputyDirector', "Direktor o'rinbosari"),
    ('HeadOfDepartment', "Bo'lim/Kafedra mudiri"),
    ('Teacher', "O'qituvchi"),
    ('Methodist', "Metodist"),
    ('Accountant', "Buxgalter"),
    ('Librarian', "Kutubxonachi"),
    ('Psychologist', "Psixolog"),
    ('Secretary', "Kotib"),
    ('FacilitiesHead', "Xo'jalik bo'limi boshlig'i"),
    ('FacilitiesStaff', "Xo'jalik xodimi"),
    ('Technical', "Texnik xodim"),
]

@login_required
def profile_view(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and (not p_form or p_form.is_valid()):
            u_form.save()
            if p_form:
                p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile) if profile else None

    # Get user certificates
    certificates = request.user.certificates.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'certificates': certificates,
    }
    return render(request, 'users/profile.html', context)

@login_required
def certificate_create(request):
    """Add a new certificate."""
    if request.method == 'POST':
        name = request.POST.get('name')
        issuer = request.POST.get('issuer')
        date_issued = request.POST.get('date_issued')
        expiry_date = request.POST.get('expiry_date') or None
        file = request.FILES.get('file')
        
        if name and date_issued:
            Certificate.objects.create(
                employee=request.user,
                name=name,
                issuer=issuer,
                date_issued=date_issued,
                expiry_date=expiry_date,
                file=file
            )
            messages.success(request, 'Sertifikat muvaffaqiyatli qo\'shildi!')
        else:
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')
        
        return redirect('profile')
    
    return render(request, 'users/certificate_form.html')

@login_required
def certificate_delete(request, certificate_id):
    """Delete a certificate."""
    certificate = get_object_or_404(Certificate, id=certificate_id, employee=request.user)
    certificate.delete()
    messages.success(request, 'Sertifikat o\'chirildi.')
    return redirect('profile')


# ---- User Management (Superadmin only) ----

def superadmin_required(view_func):
    """Decorator: faqat superadmin kirishi mumkin."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Bu sahifaga kirish uchun huquqingiz yo'q.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@superadmin_required
def user_management(request):
    """Barcha xodimlar ro'yxati va ularning rollari."""
    users = User.objects.exclude(is_superuser=True).order_by('last_name', 'first_name')
    return render(request, 'users/user_management.html', {
        'users': users,
        'school_roles': SCHOOL_ROLES,
    })


@login_required
@superadmin_required
def user_create(request):
    """Yangi xodim yaratish."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()

        if not username or not password:
            messages.error(request, "Username va parol majburiy.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' foydalanuvchisi allaqachon mavjud.")
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            # Assign role (Group)
            user.groups.clear()
            if role:
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)
            # Create EmployeeProfile automatically
            EmployeeProfile.objects.get_or_create(user=user)
            messages.success(request, f"{first_name} {last_name} muvaffaqiyatli qo'shildi.")
            return redirect('user_management')

    return render(request, 'users/user_form.html', {
        'school_roles': SCHOOL_ROLES,
        'action': 'create',
    })


@login_required
@superadmin_required
def user_edit(request, user_id):
    """Xodimni tahrirlash va rolini o'zgartirish."""
    employee = get_object_or_404(User, id=user_id)
    current_role = employee.groups.first().name if employee.groups.exists() else ''

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name', employee.first_name).strip()
        employee.last_name = request.POST.get('last_name', employee.last_name).strip()
        new_password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()

        if new_password:
            employee.set_password(new_password)
        employee.save()

        employee.groups.clear()
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            employee.groups.add(group)

        messages.success(request, f"{employee.get_full_name() or employee.username} yangilandi.")
        return redirect('user_management')

    return render(request, 'users/user_form.html', {
        'employee': employee,
        'school_roles': SCHOOL_ROLES,
        'current_role': current_role,
        'action': 'edit',
    })


@login_required
@superadmin_required
def user_delete(request, user_id):
    """Xodimni o'chirish."""
    employee = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        name = employee.get_full_name() or employee.username
        employee.delete()
        messages.success(request, f"{name} o'chirildi.")
        return redirect('user_management')
    return render(request, 'users/user_confirm_delete.html', {'employee': employee})
