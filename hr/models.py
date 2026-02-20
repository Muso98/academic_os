from django.db import models
from django.conf import settings
from core.models import UUIDModel
from core.fields import EncryptedField
from django.utils.translation import gettext_lazy as _

class EmployeeProfile(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile', verbose_name=_("Foydalanuvchi"))
    passport_number = EncryptedField(blank=True, null=True, verbose_name=_("Pasport raqami/JShSHIR"))
    salary = EncryptedField(blank=True, null=True, help_text=_("Oylik maosh (UZS)"), verbose_name=_("Oylik maosh"))
    employment_contract_end_date = models.DateField(null=True, blank=True, verbose_name=_("Shartnoma tugash sanasi"))
    qualification_category = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Malaka toifasi / Aniq vazifasi"))
    
    # New fields for profile polish
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, verbose_name=_("Qiyofacha (Avatar)"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("Tarjimayi hol (Bio)"))
    phone_number = models.CharField(max_length=20, blank=True, verbose_name=_("Telefon raqami"))
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Manzil"))

    # Storing certificates as a simple JSON list for now (e.g., [{"name": "IELTS", "date": "2024-01-01"}])
    certificates = models.JSONField(default=list, blank=True, verbose_name=_("Sertifikatlar (JSON)"))

    class Meta:
        verbose_name = _('Xodim Profili')
        verbose_name_plural = _('Xodimlar Profillari')

    def __str__(self):
        return f"Profile: {self.user.username}"

class KPIIndicator(UUIDModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    description = models.TextField(blank=True, verbose_name=_("Tavsif"))
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("Ushbu indikator uchun beriladigan ball"), verbose_name=_("Vazni"))
    criteria = models.TextField(help_text=_("Ushbu KPI ga erishish qoidalari"), verbose_name=_("Mezonlar"))

    class Meta:
        verbose_name = _('KPI Indikatori')
        verbose_name_plural = _('KPI Indikatorlari')

    def __str__(self):
        return f"{self.name} ({self.weight})"

class KPIRecord(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kpi_records', verbose_name=_("Foydalanuvchi"))
    indicator = models.ForeignKey(KPIIndicator, on_delete=models.CASCADE, related_name='records', verbose_name=_("Indikator"))
    date_achieved = models.DateField(verbose_name=_("Erishilgan sana"))
    score_obtained = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Olingan ball"))
    proof_document = models.FileField(upload_to='kpi_proofs/', blank=True, null=True, verbose_name=_("Isbotlovchi hujjat"))
    verified = models.BooleanField(default=False, verbose_name=_("Tasdiqlangan"))

    class Meta:
        verbose_name = _('KPI Yozuvi (Natijasi)')
        verbose_name_plural = _('KPI Yozuvlari (Natijalari)')

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
        verbose_name = _("Sertifikat")
        verbose_name_plural = _("Sertifikatlar")
    
    def __str__(self):
        return f"{self.name} - {self.employee.get_full_name() or self.employee.username}"
    
    @property
    def is_expired(self):
        """Check if certificate has expired."""
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False

class CertificateSequence(UUIDModel):
    """
    Tracks the sequence number for generated certificates per year.
    Useful for dynamically generating the serial numbers like '2026 yil ... 1-son'.
    """
    year = models.IntegerField(unique=True, help_text=_("Yil (Masalan: 2026)"), verbose_name=_("Yil"))
    last_number = models.PositiveIntegerField(default=0, help_text=_("Oxirgi berilgan ma'lumotnoma raqami"), verbose_name=_("Oxirgi raqam"))

    class Meta:
        verbose_name = _("Ma'lumotnoma Tartib Raqami")
        verbose_name_plural = _("Ma'lumotnoma Tartib Raqamlari")

    def __str__(self):
        return f"{self.year} yil - oxirgi raqam: {self.last_number}"
    
    @classmethod
    def get_next_number(cls, current_year):
        sequence, created = cls.objects.get_or_create(year=current_year)
        sequence.last_number += 1
        sequence.save()
        return sequence.last_number
