from django.db import models
from django.conf import settings
from core.models import UUIDModel
from core.fields import EncryptedField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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


class SickLeave(UUIDModel):
    """
    Xodimning kasallik varaqasi: xodim faylni yuklaydi,
    HR bo'limi ko'rib chiqib kasallik kunlarini tasdiqlaydi.
    """
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, _("Kutilmoqda")),
        (STATUS_APPROVED, _("Tasdiqlandi")),
        (STATUS_REJECTED, _("Rad etildi")),
    ]

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sick_leaves',
        verbose_name=_("Xodim")
    )
    start_date = models.DateField(verbose_name=_("Boshlash sanasi"))
    end_date = models.DateField(verbose_name=_("Tugash sanasi"))
    certificate_file = models.FileField(
        upload_to='sick_leaves/',
        verbose_name=_("Kasallik varaqasi (fayl)")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_("Holat")
    )
    hr_note = models.TextField(
        blank=True,
        verbose_name=_("HR izohi")
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviewed_sick_leaves',
        verbose_name=_("Ko'rib chiqqan HR")
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yuborilgan vaqt"))
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Ko'rib chiqilgan vaqt"))

    class Meta:
        verbose_name = _("Kasallik Varaqasi")
        verbose_name_plural = _("Kasallik Varaqalari")
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.employee.get_full_name() or self.employee.username} | {self.start_date} - {self.end_date} | {self.get_status_display()}"

    @property
    def days_count(self):
        """Kasallik kunlari soni."""
        return (self.end_date - self.start_date).days + 1
