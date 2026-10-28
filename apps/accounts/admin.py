from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "sport_id", "is_active")
    list_filter = ("role", "is_active", "sport_id")
    search_fields = ("username", "email", "first_name", "last_name")
    
    # Add our custom fields to the admin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('AshesiScore Permissions', {'fields': ('role', 'sport_id')}),
    )