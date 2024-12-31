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

    def is_valid(self, *, raise_exception=False):
        # ignore check of already existing customer
        return True

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

    # write a create or update method for the customer serializer
    def create_or_update(self, validated_data):
        """
        Create or update a customer based on the validated data.
        """
        # Get the client_id from the validated data
        client_id = validated_data.get("client_id")
        # Get the customer_id from the validated data
        customer_id = validated_data.get("customer_id")
        # Get the contacts from the validated data
        contacts = validated_data.get("contacts")
        # Get the is_vip from the validated data
        is_vip = validated_data.get("is_vip")
        # Get the custom_fields from the validated data
        custom_fields = validated_data.get("custom_fields")
        # Get the is_synced from the validated data
        is_synced = validated_data.get("is_synced")
        # Get the created_at from the validated data
        created_at = validated_data.get("created_at")
        # Get the updated_at from the validated data
        updated_at = validated_data.get("updated_at")
        # Check if the customer already exists
        try:
            customer = Customer.objects.get(client_id=client_id)
            # Update the customer with the new data
            customer.customer_id = customer_id
            customer.contacts = contacts
            customer.is_vip = is_vip
            customer.custom_fields = custom_fields
            customer.is_synced = is_synced
            customer.created_at = created_at
            customer.updated_at = updated_at
            customer.save()
        except Customer.DoesNotExist:
            # Create a new customer with the data
            customer = Customer.objects.create(
                client_id=client_id,
                customer_id=customer_id,
                contacts=contacts,
                is_vip=is_vip,
                custom_fields=custom_fields,
                is_synced=is_synced,
                created_at=created_at,
                updated_at=updated_at,
            )
        return customer


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
                    print("CUSTOMER ID", customer_id)
                    customer = Customer.objects.get(id=customer_id.id)
                except Customer.DoesNotExist:
                    # Handle gracefully: Log, or allow it to be saved as None (if customer_id is optional)
                    pass  # Do nothing, allow it

            # Set `is_synced` to False when creating a new invoice
            self.validated_data["is_synced"] = False

            # Create a new instance
            return super().save(**kwargs)

    def is_valid(self, *, raise_exception=False):
        # ignore check of already existing invoice
        return True

    def create_or_update(self, validated_data):
        """
        Create or update an invoice based on the validated data.
        """
        # Get the client_id from the validated data
        client_id = validated_data.get("client_id")
        # Get the customer_id from the validated data
        customer_id = validated_data.get("customer_id")
        # Get the amount_owning from the validated data
        amount_owning = validated_data.get("amount_owning")
        # Get the amount_paid from the validated data
        amount_paid = validated_data.get("amount_paid")
        # Get the due_date from the validated data
        due_date = validated_data.get("due_date")
        # Get the is_paid from the validated data
        is_paid = validated_data.get("is_paid")
        # Get the is_synced from the validated data
        is_synced = validated_data.get("is_synced")
        # Get the created_at from the validated data
        created_at = validated_data.get("created_at")
        # Get the updated_at from the validated data
        updated_at = validated_data.get("updated_at")
        # Check if the invoice already exists
        try:
            invoice = Invoice.objects.get(client_id=client_id)
            # Update the invoice with the new data
            invoice.customer_id = customer_id
            invoice.amount_owning = amount_owning
            invoice.amount_paid = amount_paid
            invoice.due_date = due_date
            invoice.is_paid = is_paid
            invoice.is_synced = is_synced
            invoice.created_at = created_at
            invoice.updated_at = updated_at
            invoice.save()
        except Invoice.DoesNotExist:
            # Create a new invoice with the data
            invoice = Invoice.objects.create(
                client_id=client_id,
                customer_id=customer_id,
                amount_owning=amount_owning,
                amount_paid=amount_paid,
                due_date=due_date,
                is_paid=is_paid,
                is_synced=is_synced,
                created_at=created_at,
                updated_at=updated_at,
            )
        return invoice
