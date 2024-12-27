from django.db import models

# import user base model django
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    active = models.BooleanField(default=True)
    iodm_token = models.CharField(max_length=255, blank=True, null=True)
    iodm_api_key = models.CharField(max_length=255, blank=True, null=True)
    abtract_secret_key = models.CharField(max_length=255, blank=True, null=True)

    # Modify groups and user_permissions to avoid conflicts with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name="main_user_set",  # Set a custom reverse related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="main_user_permissions_set",  # Set a custom reverse related name
        blank=True,
    )


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    contacts = models.JSONField()
    is_vip = models.BooleanField(default=False)
    custom_fields = models.JSONField()
    is_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    id = models.IntegerField(primary_key=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_owning = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    is_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
