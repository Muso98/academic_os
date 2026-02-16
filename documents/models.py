from django.db import models
from django.conf import settings
from core.models import UUIDModel

class Order(UUIDModel):
    """
    Internal Orders (Buyruqlar) issued by Admin/Director.
    """
    title = models.CharField(max_length=255, verbose_name="Buyruq mavzusi")
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Buyruq raqami")
    file = models.FileField(upload_to='orders/', verbose_name="Buyruq fayli (PDF/Word)")
    date_signed = models.DateField(verbose_name="Imzolangan sana")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: visibility level or target audience could be added later
    
    class Meta:
        ordering = ['-date_signed']
        verbose_name = "Buyruq"
        verbose_name_plural = "Buyruqlar"

    def __str__(self):
        return f"{self.order_number} - {self.title}"

class Report(UUIDModel):
    """
    Reports (Hisobotlar) submitted by Teachers.
    """
    REPORT_TYPES = (
        ('QUARTERLY', 'Choraklik Hisobot'),
        ('ANNUAL', 'Yillik Hisobot'),
        ('OTHER', 'Boshqa'),
    )

    STATUS_CHOICES = (
        ('SUBMITTED', 'Topshirildi (Submitted)'),
        ('APPROVED', 'Tasdiqlandi (Approved)'),
        ('REJECTED', 'Rad etildi (Rejected)'),
    )

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255, verbose_name="Hisobot nomi")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='QUARTERLY')
    file = models.FileField(upload_to='reports/', verbose_name="Hisobot fayli")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    admin_comment = models.TextField(blank=True, null=True, verbose_name="Admin izohi (Rad etish sababi)")
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Hisobot"
        verbose_name_plural = "Hisobotlar"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
