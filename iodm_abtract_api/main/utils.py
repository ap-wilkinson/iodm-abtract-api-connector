from django.utils import timezone
import requests
from .serializer import CustomerSerializer, InvoiceSerializer
from .models import Customer, Invoice, User


def get_client_contacts(secret_key):
    # this is for abtract api
    url = (
        "https://www.abtraconline.com/api/abtraccustomapi/GetClientContactList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    data = response.json()
    return data


def get_client_adress(secret_key):
    # this is for abtract api
    url = (
        " https://www.abtraconline.com/api/abtraccustomapi/GetClientAddressList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    data = response.json()
    return data


def get_client_adress_by_id(adress_data, client_adress_id):
    # given the adress data and the client adress id, return the client adress
    for adress in adress_data:
        if adress and adress["ClientAddressID"] == client_adress_id:
            return adress


def create_customer_payload(secret_key, client_contact, user_id):
    customers = []
    customer_serializer_payload = []
    # get all client adress
    all_clients_adress = get_client_adress(secret_key)

    for contact in client_contact:
        client_adress_id = contact.get("AddressID")
        client_adress = get_client_adress_by_id(all_clients_adress, client_adress_id)
        customer = {
            "CustomerCode": str(contact.get("ClientID")),
            "CompanyName": contact.get("ClientName"),
            "DisplayName": contact.get("ClientName"),
            "TaxNumber": "",
            "SecondaryTaxNumber": "",
            "IsVip": "false",
            "Contacts": [
                {
                    "FirstName": contact.get("FirstName"),
                    "LastName": contact.get("SecondName"),
                    "AddressLine1": (client_adress or {}).get("Address1", ""),
                    "AddressLine2": (client_adress or {}).get("Address2", ""),
                    "City": (client_adress or {}).get("Address3", ""),
                    "State": (client_adress or {}).get("Address4", ""),
                    "Postcode": (client_adress or {}).get("AddressPostCode", ""),
                    "Country": "AU",  # might need to hard code in
                    "Email": contact.get("Email"),
                    "MobileNumber": contact.get("Mobile"),
                    "PhoneNumber": contact.get("Phone"),
                }
            ],
        }
        contacts_dict = {
            f"contact{index+1}": {  # Dynamic key for each contact
                "FirstName": contact.get("FirstName"),
                "LastName": contact.get("SecondName"),
                "AddressLine1": (client_adress or {}).get("Address1", ""),
                "AddressLine2": (client_adress or {}).get("Address2", ""),
                "City": (client_adress or {}).get("Address3", ""),
                "State": (client_adress or {}).get("Address4", ""),
                "Postcode": (client_adress or {}).get("AddressPostCode", ""),
                "Country": "AU",  # might need to hard code in
                "Email": contact.get("Email"),
                "MobileNumber": contact.get("Mobile"),
                "PhoneNumber": contact.get("Phone"),
            }
            for index, contact in enumerate(
                [contact]
            )  # Loop over contacts if more than one
        }
        # create a serializer payload for the customer
        customer_serializer_payload.append(
            {
                "id": contact.get("ClientID"),
                "client_id": user_id,  # Assuming user_id is already defined
                "contacts": contacts_dict,  # Pass the dictionary of contacts here
                "is_vip": contact.get("IsVip", "false").lower()
                == "true",  # Convert IsVip to boolean
                "custom_fields": {},  # Empty custom fields
                "is_synced": False,  # Default value
            }
        )

        customers.append(customer)
    return customers, customer_serializer_payload


def get_invoices(secret_key):
    # this is for abtract api
    url = (
        "https://www.abtraconline.com/api/abtraccustomapi/GetInvoiceList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    data = response.json()
    return data


def create_invoice_payload(user_id, invoices):
    invoice_list = []
    invoice_serializer_payload = []
    for invoice in invoices:
        amount_owing = "0"
        amount_paid = "0"
        if invoice.get("InvoicePaid"):
            amount_owing = "0"
        else:
            total_amount = (invoice or {}).get("OriginalAmount", 0)
            amount_paid = (invoice or {}).get("AmountPaidInclTax", 0)
            amount_owing = str(total_amount - amount_paid)
        invoice_payload = {
            "InvoiceCode": str(invoice.get("InvoiceID")),
            "Number": str(invoice.get("InvoiceNumber")),
            "CreatedDate": invoice.get("InvoiceDate"),
            "DueDate": invoice.get("DueDate"),
            "OriginalAmount": str(invoice.get("OriginalAmount")),
            "AmountOwing": amount_owing,
            "Customer": {
                "CustomerCode": str(invoice.get("ClientID")),
            },
        }
        invoice_serializer_payload.append(
            {
                "id": invoice.get("InvoiceID"),
                "client_id": user_id,
                "customer_id": invoice.get("Client").get("ClientID"),
                "amount_owning": amount_owing,
                "amount_paid": amount_paid,
                "due_date": invoice.get("DueDate"),
                "created_at": invoice.get("InvoiceDate"),
                "is_paid": (invoice or {}).get("AddressPostCode", False),
                "is_synced": False,
            }
        )
        invoice_list.append(invoice_payload)
    return invoice_list, invoice_serializer_payload


def get_access_token(iodm_access_key, iodm_secret_key):
    url = "https://api.sandbox.iodmconnectonline.com/authorise/token"
    body = {"Key": iodm_access_key, "Token": iodm_secret_key}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    print("Data", data)
    return data.get("AccessToken")


def save_customer(access_token, customers):
    # get length of customers and divide it by 99 to get the number of pages
    # then loop through the pages and save the customers
    customers_per_page = 99
    number_of_pages = len(customers) // customers_per_page
    for page in range(number_of_pages):
        start = page * customers_per_page
        end = (page + 1) * customers_per_page
        body = {"Customers": customers[start:end]}

        url = "https://api.sandbox.iodmconnectonline.com/customer"
        headers = {
            "Authorization": f"{access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print("Customer saved")
            continue
        print("REsp", response.json())
        print("Customer not saved")


def save_invoice(access_token, invoices):
    # if the length of invoices is greater than 99, divide it by 99 and loop through the pages
    # then save the invoices
    invoices_per_page = 99
    number_of_pages = len(invoices) // invoices_per_page
    for page in range(number_of_pages):
        start = page * invoices_per_page
        end = (page + 1) * invoices_per_page
        body = {"Invoices": invoices[start:end]}
        url = "https://api.sandbox.iodmconnectonline.com/invoice"
        headers = {
            "Authorization": f"{access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print("Invoice saved")
        else:
            print("body", body["Invoices"][0])
            print("REsp", response.json())
            print("Invoice not saved")


def save_data_to_db(customers, invoices):
    for customer in customers:
        serializer = CustomerSerializer(data=customer)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return

    for invoice in invoices:
        serializer = InvoiceSerializer(data=invoice)
        if serializer.is_valid():
            serializer.save()

        else:
            print(serializer.errors)
            return


def get_data_not_synced():
    customers = Customer.objects.filter(is_synced=False)
    invoices = Invoice.objects.filter(is_synced=False)
    return customers, invoices


def update_data_synced(customers, invoices):
    for customer in customers:
        customer.is_synced = True
        customer.save()
    for invoice in invoices:
        invoice.is_synced = True
        invoice.save()


def main():
    # for each user in the database get values and call functions and save data
    # get all users with staff status false
    users = User.objects.filter(is_staff=False)

    for user in users:
        secret_key = user.abtract_secret_key
        client_contacts = get_client_contacts(secret_key)
        # print timestampe
        print(timezone.now())
        print("-=-------=-=-= client_contacts_done")
        customers, customer_serializer_payload = create_customer_payload(
            secret_key, client_contacts, user.id
        )
        print(timezone.now())
        print("-=-------=-=-= customers_done")
        invoices = get_invoices(secret_key)
        print(timezone.now())
        print("-=-------=-=-= invoices_done")
        invoices, invoice_serializer_payload = create_invoice_payload(user.id, invoices)
        print(timezone.now())
        print("-=-------=-=-= invoices_payload_done")
        print("api key and token ", user.iodm_api_key, user.iodm_token)
        access_token = get_access_token(user.iodm_api_key, user.iodm_token)
        print(timezone.now())
        # save customer to db
        save_data_to_db(customer_serializer_payload, invoice_serializer_payload)
        print(timezone.now())
        print("-=-------=-=-= save_data_to_db_done")
        # save data to iodm
        # customers, invoices = get_data_not_synced()
        print(timezone.now())
        print("-=-------=-=-= get_data_not_synced_done")
        print(access_token, "access_token")
        save_customer(access_token, customers)
        print(timezone.now())
        print("-=-------=-=-= save_customer_done")

        save_invoice(access_token, invoices)
        print(timezone.now())
        customers = Customer.objects.filter(is_synced=False)
        invoices = Invoice.objects.filter(is_synced=False)
        update_data_synced(customers, invoices)
        print(timezone.now())
        print("-=-------=-=-= update_data_synced_done")
        print("Data Synced")
