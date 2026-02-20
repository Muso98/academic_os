from django.urls import path
from . import views

urlpatterns = [
    path('employee/<uuid:pk>/certificate/print/', views.print_employee_certificate, name='print_employee_certificate'),
    path('verify/<uuid:pk>/', views.verify_employee_certificate, name='verify_certificate'),
]
