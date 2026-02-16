from django.db import models
from django.conf import settings
from core.models import UUIDModel
from core.fields import EncryptedField

class EmployeeProfile(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    passport_number = EncryptedField(blank=True, null=True)
    salary = EncryptedField(blank=True, null=True, help_text="Monthly salary in UZS")
    employment_contract_end_date = models.DateField(null=True, blank=True)
    qualification_category = models.CharField(max_length=100, blank=True, null=True)
    
    # New fields for profile polish
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    # Storing certificates as a simple JSON list for now (e.g., [{"name": "IELTS", "date": "2024-01-01"}])
    certificates = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

class KPIIndicator(UUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Points awarded for this indicator")
    criteria = models.TextField(help_text="Rules for achieving this KPI")

    def __str__(self):
        return f"{self.name} ({self.weight})"

class KPIRecord(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kpi_records')
    indicator = models.ForeignKey(KPIIndicator, on_delete=models.CASCADE, related_name='records')
    date_achieved = models.DateField()
    score_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    proof_document = models.FileField(upload_to='kpi_proofs/', blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.indicator.name} ({self.score_obtained})"

class Certificate(UUIDModel):
    """
    Employee certificates and awards.
    Replaces the JSON field in EmployeeProfile.
    """
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255, verbose_name="Sertifikat nomi", help_text="Masalan: IELTS 7.5, CEFR C1")
    issuer = models.CharField(max_length=255, blank=True, verbose_name="Beruvchi tashkilot", help_text="Masalan: British Council")
    date_issued = models.DateField(verbose_name="Berilgan sana")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Amal qilish muddati")
    file = models.FileField(upload_to='certificates/', blank=True, null=True, verbose_name="Sertifikat fayli (PDF/JPG)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_issued']
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
    
    def __str__(self):
        return f"{self.name} - {self.employee.get_full_name() or self.employee.username}"
    
    @property
    def is_expired(self):
        """Check if certificate has expired."""
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False
