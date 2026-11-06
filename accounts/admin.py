from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "is_staff"]
    
    fieldsets = UserAdmin.fieldsets + (
        ("School Profile", {"fields": ("role", "course")}),
    )
