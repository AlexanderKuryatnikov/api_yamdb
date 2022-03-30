from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'role')
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'role')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'bio')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff',
                       'is_superuser', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'email', 'role')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'bio')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
