from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_verified', 'is_active')  # Update this to include valid fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'dob', 'occupation', 'institution')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_verified', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
        ),
    )
