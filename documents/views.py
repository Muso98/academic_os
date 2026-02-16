from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Order, Report
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

# --- Access Checks ---
def is_admin(user):
    return user.is_superuser or user.is_staff

# --- Internal Orders (Buyruqlar) ---

@login_required
def order_list(request):
    """
    List all internal orders.
    Visible to all staff.
    """
    orders = Order.objects.all()
    return render(request, 'documents/order_list.html', {'orders': orders})

@user_passes_test(is_admin)
def order_create(request):
    """
    Admin only: Upload a new order.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        order_number = request.POST.get('order_number')
        date_signed = request.POST.get('date_signed')
        file = request.FILES.get('file')

        if title and order_number and date_signed and file:
            Order.objects.create(
                title=title,
                order_number=order_number,
                date_signed=date_signed,
                file=file
            )
            messages.success(request, "Buyruq muvaffaqiyatli yuklandi!")
            return redirect('order_list')
        else:
            messages.error(request, "Iltimos, barcha maydonlarni to'ldiring.")

    return render(request, 'documents/order_form.html')

# --- Reports (Hisobotlar) ---

@login_required
def report_list(request):
    """
    List reports.
    - Admin: Sees ALL reports.
    - Teacher: Sees OWN reports.
    """
    user = request.user
    if is_admin(user):
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(teacher=user)
    
    return render(request, 'documents/report_list.html', {'reports': reports, 'is_admin': is_admin(user)})

@login_required
def report_create(request):
    """
    Teacher: Upload a new report.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        report_type = request.POST.get('report_type')
        file = request.FILES.get('file')

        if title and report_type and file:
            Report.objects.create(
                teacher=request.user,
                title=title,
                report_type=report_type,
                file=file,
                status='SUBMITTED'
            )
            messages.success(request, "Hisobot yuborildi!")
            return redirect('report_list')
        else:
            messages.error(request, "Barcha maydonlarni to'ldiring.")

    return render(request, 'documents/report_form.html')

@user_passes_test(is_admin)
def report_update_status(request, report_id):
    """
    Admin: Approve or Reject a report.
    """
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        comment = request.POST.get('admin_comment')
        
        if status in ['APPROVED', 'REJECTED']:
            report.status = status
            report.admin_comment = comment
            report.save()
            
            # Optional: Notify teacher about status change (TODO)
            messages.success(request, f"Hisobot holati o'zgartirildi: {status}")
            
    return redirect('report_list')
