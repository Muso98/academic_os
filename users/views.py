from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from hr.models import EmployeeProfile, Certificate

@login_required
def profile_view(request):
    try:
        profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile) if profile else None

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
