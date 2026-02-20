from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User
from hr.models import EmployeeProfile

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = _("Xodim faoliyati va shaxsiy tafsilotlari")
    fk_name = 'user'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups')

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    inlines = (EmployeeProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'get_groups', 'is_staff')
    list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Shaxsiy ma\'lumotlar (Foydalanuvchi)'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Guruhlar va Ruxsatlar (Vazifasi)'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'groups'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        # Override Django's default behavior that hides inlines on user creation
        return super(BaseUserAdmin, self).get_inline_instances(request, obj)

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = _("Vazifasi (Guruhlar)")

admin.site.register(User, UserAdmin)
