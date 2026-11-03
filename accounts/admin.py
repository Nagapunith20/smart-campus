
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        'username',
        'email',
        'role',
        'student_id',
        'department',
        'year',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('SMART CAMPUS Details', {
            'fields': (
                'role',
                'student_id',
                'department',
                'year',
                'phone_number',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SMART CAMPUS Details', {
            'fields': (
                'email',
                'role',
                'student_id',
                'department',
                'year',
                'phone_number',
            )
        }),
    )
