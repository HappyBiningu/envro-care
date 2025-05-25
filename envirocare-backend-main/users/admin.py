from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    list_per_page = 30
    search_fields = ("email", "username")
    fieldsets = (
        (None, {"fields": ("username",)}), 
        ("Personal Info",{"fields": ("first_name","last_name","email","phone_number",
                                     "sex","id_number","date_of_birth","profile_photo")},),
        ("Permissions",{"fields": ("is_active","is_staff","is_superuser",
                                    "low_permissions", "medium_permissions", "high_permissions", "super_permissions", "ultra_permissions",
                                    "extreme_permissions"),},),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ("date_joined","is_active","is_staff","is_superuser")
