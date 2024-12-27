# create serializer for the model
from django.utils import timezone
from rest_framework import serializers
from .models import User, Customer, Invoice


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "active",
            "iodm_token",
            "iodm_api_key",
            "abtract_secret_key",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "client_id",
            "contacts",
            "is_vip",
            "custom_fields",
            "is_synced",
            "created_at",
            "updated_at",
        ]

    # Example validation for contacts (if needed)
    def validate_contacts(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Contacts must be a dictionary.")
        return value

    def save(self, **kwargs):
        """
        Override the save method to check if the customer exists.
        If it exists, compare values and set `is_synced` to False if any values are changed.
        If it doesn't exist, create a new customer.
        """
        # Check if customer with this id already exists (for update)
        instance = self.instance

        # Check if we're updating an existing customer
        if instance:
            # The customer exists, compare values
            for field, new_value in self.validated_data.items():
                old_value = getattr(instance, field, None)
                if old_value != new_value:  # If any field value has changed
                    instance.is_synced = False  # Set is_synced to False
                    break  # No need to check further once we detect a change
            # Now update the instance with new values
            for field, new_value in self.validated_data.items():
                setattr(instance, field, new_value)
            instance.save()
            return instance  # Return the updated instance

        # If the customer doesn't exist (creating new customer)
        else:
            # Set `is_synced` to False when creating a new customer
            self.validated_data["is_synced"] = False

            # Create a new instance
            return super().save(**kwargs)


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "client_id",
            "customer_id",
            "amount_owning",
            "amount_paid",
            "due_date",
            "is_paid",
            "is_synced",
            "created_at",
            "updated_at",
        ]

    def validate_amount_owning(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount owing cannot be negative.")
        return value

    def save(self, **kwargs):
        """
        Override the save method to check if the invoice exists.
        If it exists, compare values and set `is_synced` to False if any values are changed.
        If it doesn't exist, create a new invoice.
        """
        # Check if invoice with this id already exists (for update)
        instance = self.instance

        # Check if we're updating an existing invoice
        if instance:
            # The invoice exists, compare values
            for field, new_value in self.validated_data.items():
                old_value = getattr(instance, field, None)
                if old_value != new_value:  # If any field value has changed
                    instance.is_synced = False  # Set is_synced to False
                    break  # No need to check further once we detect a change
            # Now update the instance with new values
            for field, new_value in self.validated_data.items():
                setattr(instance, field, new_value)
            instance.save()
            return instance  # Return the updated instance

        # If the invoice doesn't exist (creating new invoice)
        else:
            # Optionally check if customer_id exists and is valid if required.
            # This is only if you want to make sure the customer_id is valid when creating a new invoice
            customer_id = self.validated_data.get("customer_id")
            if customer_id:
                try:
                    customer = Customer.objects.get(id=customer_id)
                except Customer.DoesNotExist:
                    # Handle gracefully: Log, or allow it to be saved as None (if customer_id is optional)
                    pass  # Do nothing, allow it to be saved as `None` (or raise warning if needed)

            # Set `is_synced` to False when creating a new invoice
            self.validated_data["is_synced"] = False

            # Create a new instance
            return super().save(**kwargs)
