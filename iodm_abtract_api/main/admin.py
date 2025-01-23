from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django_search_filters import SearchFilter
from .models import User, Customer, Invoice


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "iodm_token",
                    "iodm_api_key",
                    "abtract_secret_key",
                    "abtract_start_page",
                    "abtract_page_size",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "iodm_token",
                    "iodm_api_key",
                    "abtract_secret_key",
                    "abtract_start_page",
                    "abtract_page_size",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
# admin.site.register(Customer)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        # "client_id",
        "client_name",
        "client_code",
        "is_vip",
        "is_synced",
        "created_at",
        "updated_at",
    ]
    list_filter = ["client_id", "is_vip", "is_synced"]
    search_fields = ["id", "client_name", "client_code"]
    list_per_page = 30
    list_max_show_all = 100
# admin.site.register(Invoice)
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        # "client_id",
        "client_code",
        "customer_id",
        "amount_owning",
        "amount_paid",
        "due_date",
        "is_paid",
        "is_synced",
        "created_at",
        "updated_at",
    ]
    list_filter = ["client_id", "customer_id", "is_paid", "is_synced"]
    search_fields = ["id", "client_code", "amount_owning", "amount_paid"]
    list_per_page = 30
    list_max_show_all = 100

