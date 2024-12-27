from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Invoice


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("iodm_token", "iodm_api_key", "abtract_secret_key")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("iodm_token", "iodm_api_key", "abtract_secret_key")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(Invoice)
