from django.urls import path
from . import views

urlpatterns = [
    path('employee/<uuid:pk>/certificate/print/', views.print_employee_certificate, name='print_employee_certificate'),
    path('verify/<uuid:pk>/', views.verify_employee_certificate, name='verify_certificate'),
    # Sick Leave
    path('sick-leave/submit/', views.sick_leave_submit, name='sick_leave_submit'),
    path('sick-leave/my/', views.sick_leave_list, name='sick_leave_list'),
    path('sick-leave/hr/', views.sick_leave_hr_list, name='sick_leave_hr_list'),
    path('sick-leave/<uuid:pk>/review/', views.sick_leave_review, name='sick_leave_review'),
]
