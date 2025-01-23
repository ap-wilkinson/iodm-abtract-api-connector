from django.utils import timezone
import requests
from .serializer import CustomerSerializer, InvoiceSerializer
from .models import Customer, Invoice, User

iodm_url = "https://api.sandbox.iodmconnectonline.com/"
abtract_url = "https://www.abtraconline.com/api/abtraccustomapi"
global invalid_cust 
invalid_cust = []
def get_clients(secret_key):
    # this is for abtract api
    url = (
        "https://www.abtraconline.com/api/abtraccustomapi/GetClientsList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    client_data = response.json()
    #for each client create a dict with key value ClientID and value is ClientCode 
    all_clients = {}
    for client in client_data:
        all_clients[client.get("ClientID")] = {
            "ClientCode": client.get("ClientCode"),
            "ClientName": client.get("ClientName"),
            "Comment": client.get("Comment"),
        }
    return all_clients


def get_client_contacts(secret_key):
    # this is for abtract api
    url = (
        f"{abtract_url}/GetClientContactList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    all_client_contacts = {}
    clients_contacts = response.json()
    for contact in clients_contacts:
        #aginst one clientId there can be multiple contacts 
        #so we will create a list of contacts for each clientId
        if contact.get("ClientID") not in all_client_contacts:
            all_client_contacts[contact.get("ClientID")] = []
        contact_data = {
            "FirstName": contact.get("FirstName"),
            "SecondName": contact.get("SecondName"),
            "Email": contact.get("Email"),
            "Phone": contact.get("Phone"),
            "Mobile": contact.get("Mobile"),
            "ClientName": contact.get("ClientName"),
            "AddressID": contact.get("AddressID"),
            "IsVip": contact.get("IsVip"),
        }
        all_client_contacts[contact.get("ClientID")].append(contact_data)


    return all_client_contacts


def get_client_adress(secret_key):
    # this is for abtract api
    url = (
        f"{abtract_url}/GetClientAddressList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    clients_adress = response.json()
    #create a dict with key value ClientAddressID and value is the address data
    data = {}
    for adress in clients_adress:
        adress_data = {
            "ClientAddressID": adress.get("ClientAddressID"),
            "Address1": adress.get("Address1"),
            "Address2": adress.get("Address2"),
            "Address3": adress.get("Address3"),
            "Address4": adress.get("Address4"),
            "AddressPostCode": adress.get("AddressPostCode"),
        }
        data[adress.get("ClientID")] = adress_data

    return data


def get_client_adress_by_id(adress_data, client_adress_id):
    # given the adress data and the client adress id, return the client adress
    for adress in adress_data:
        if adress and adress["ClientAddressID"] == client_adress_id:
            return adress


def create_customer_payload(all_clients, clients_contacts, clients_adress, user_id):
    customers = []
    customer_serializer_payload = []
    for client_id in all_clients:
        client = all_clients[client_id]
        contacts = clients_contacts.get(client_id)
        values_missing = False 
        if not contacts:
            print(client_id, "no contact")
            values_missing = True
            #create a empty list of contacts
            
            contacts = [
                {
                    "FirstName": "N/A",
                    "SecondName": "N/A",
                    "Email": "Na@na.com",
                    "Phone": "123455689",
                    "Mobile": "123455689",

                }
            ]
        adress = clients_adress.get(client_id)
        if not adress or not adress.get("Address1"):
            values_missing = True
            print(client_id, "no adress")
            adress = {
                "Address1": "N/A",
                "Address2": "N/A",
                "Address3": "N/A",
                "Address4": "N/A",
                "AddressPostCode": "5555",
            }    
        if values_missing:
            invalid_cust.append(client_id)
        customer = {
            "CustomerCode": str(client.get("ClientCode")),
            "CompanyName": client.get("ClientName"),
            "DisplayName": client.get("ClientName"),
            "TaxNumber": "",
            "SecondaryTaxNumber": "",
            "IsVip": "false",
            "Contacts": [
                {
                    "FirstName": contact.get("FirstName"),
                    "LastName": contact.get("SecondName"),
                    "AddressLine1": adress.get("Address1", ""),
                    "AddressLine2": adress.get("Address2", ""),
                    "City": adress.get("Address3", ""),
                    "State": adress.get("Address4", ""),
                    "Postcode": adress.get("AddressPostCode", ""),
                    "Country": "AU",
                    "Email": contact.get("Email"),
                    "MobileNumber": contact.get("Mobile"),
                    "PhoneNumber": contact.get("Phone"),
                }
                for contact in contacts
            ],
            # "CustomFields": [
            #     {
            #         "Name": "Comment",
            #         "Value": all_clients.get("Comment", ""),
            #         }
            # ]
        }
        # if invalid_cust:
        #     print(customer)
        contacts_dict = {
            f"contact{index+1}": {  # Dynamic key for each contact
                "FirstName": contact.get("FirstName"),
                "LastName": contact.get("SecondName"),
                "AddressLine1": adress.get("Address1", ""),
                "AddressLine2": adress.get("Address2", ""),
                "City": adress.get("Address3", ""),
                "State": adress.get("Address4", ""),
                "Postcode": adress.get("AddressPostCode", ""),
                "Country": "AU",
                "Email": contact.get("Email"),
                "MobileNumber": contact.get("Mobile"),
                "PhoneNumber": contact.get("Phone"),
            }
            for index, contact in enumerate(
                contacts
            )  # Loop over contacts if more than one
        }
        # create a serializer payload for the customer
        customer_serializer_payload.append(
            {
                "customer_id": client_id,
                "client_id": user_id,  # Assuming user_id is already defined
                "client_name": client.get("ClientName"),
                "client_code": str(client.get("ClientCode")),
                "contacts": contacts_dict,  # Pass the dictionary of contacts here
                "is_vip": client.get("IsVip", "false").lower()
                == "true",  # Convert IsVip to boolean
                "custom_fields": {},  # Empty custom fields
                "is_synced": False,  # Default value
            }
        )
        customers.append(customer)

    return customers, customer_serializer_payload
    # customers = []
    # customer_serializer_payload = []
    # # get all client adress
    # all_clients_adress = get_client_adress(secret_key)

    # for contact in client_contact:
    #     client_adress_id = contact.get("AddressID")
    #     client_adress = get_client_adress_by_id(all_clients_adress, client_adress_id)
    #     print(contact, "contact")
    #     customer = {
    #         "CustomerCode": str(contact.get("ClientID")),
    #         "CompanyName": contact.get("ClientName"),
    #         "DisplayName": contact.get("ClientName"),
    #         "TaxNumber": "",
    #         "SecondaryTaxNumber": "",
    #         "IsVip": "false",
    #         "Contacts": [
    #             {
    #                 "FirstName": contact.get("FirstName"),
    #                 "LastName": contact.get("SecondName"),
    #                 "AddressLine1": (client_adress or {}).get("Address1", ""),
    #                 "AddressLine2": (client_adress or {}).get("Address2", ""),
    #                 "City": (client_adress or {}).get("Address3", ""),
    #                 "State": (client_adress or {}).get("Address4", ""),
    #                 "Postcode": (client_adress or {}).get("AddressPostCode", ""),
    #                 "Country": "AU",  # might need to hard code in
    #                 "Email": contact.get("Email"),
    #                 "MobileNumber": contact.get("Mobile"),
    #                 "PhoneNumber": contact.get("Phone"),
    #             }
    #         ],
    #     }
    #     contacts_dict = {
    #         f"contact{index+1}": {  # Dynamic key for each contact
    #             "FirstName": contact.get("FirstName"),
    #             "LastName": contact.get("SecondName"),
    #             "AddressLine1": (client_adress or {}).get("Address1", ""),
    #             "AddressLine2": (client_adress or {}).get("Address2", ""),
    #             "City": (client_adress or {}).get("Address3", ""),
    #             "State": (client_adress or {}).get("Address4", ""),
    #             "Postcode": (client_adress or {}).get("AddressPostCode", ""),
    #             "Country": "AU",  # might need to hard code in
    #             "Email": contact.get("Email"),
    #             "MobileNumber": contact.get("Mobile"),
    #             "PhoneNumber": contact.get("Phone"),
    #         }
    #         for index, contact in enumerate(
    #             [contact]
    #         )  # Loop over contacts if more than one
    #     }
    #     # create a serializer payload for the customer
    #     customer_serializer_payload.append(
    #         {
    #             "id": contact.get("ClientID"),
    #             "client_id": user_id,  # Assuming user_id is already defined
    #             "contacts": contacts_dict,  # Pass the dictionary of contacts here
    #             "is_vip": contact.get("IsVip", "false").lower()
    #             == "true",  # Convert IsVip to boolean
    #             "custom_fields": {},  # Empty custom fields
    #             "is_synced": False,  # Default value
    #         }
    #     )

    #     customers.append(customer)
    # return customers, customer_serializer_payload


def get_invoices(secret_key):
    # this is for abtract api
    url = (
        f"{abtract_url}/GetInvoiceList?user=&password=&secretKey="
        + secret_key
    )
    response = requests.get(url)
    data = response.json()
    return data


def get_all_invoices(secret_key, start_page, page_size):
    invoices = []
    paid_invoices = []
    for page in range(start_page, page_size):
        print("page number", page)
        url = f"{abtract_url}/GetInvoiceList?page={page}&user=&password=&secretKey={secret_key}"
        response = requests.get(url)
        data = response.json()
        for invoice in data:
            invoices.append(invoice)
    return invoices


# def update_invoices()


def get_all_invoices(secret_key, start_page, page_size):
    invoices = []
    paid_invoices = []
    for page in range(start_page, page_size):
        print("page number", page)
        url = f"{abtract_url}/GetInvoiceList?page={page}&user=&password=&secretKey={secret_key}"
        response = requests.get(url)
        data = response.json()
        for invoice in data:
            invoices.append(invoice)
    return invoices


# def update_invoices()


def create_invoice_payload(user_id, invoices, all_clients):
    invoice_list = []
    invoice_serializer_payload = []
    for invoice in invoices:
        amount_owing = 0
        amount_paid = 0
        total_amount = (invoice or {}).get("InvLinesTotalInclTax", 0)
        # if invoice.get("InvoicePaid"):
        #     continue
        # # else:
        client_id = invoice.get("Client").get("ClientID")
        customer_code = all_clients.get(client_id).get(
            "ClientCode"
        )
        if not customer_code:
            print("customer code not found")
            print(invoice.get("Client").get("ClientID"), "--------", all_clients.get(invoice.get("Client").get("ClientID")))
            continue
        amount_paid = (invoice or {}).get("AmountPaidInclTax", 0)
        amount_owing = str(total_amount - amount_paid)
        if client_id in invalid_cust:
            print("invalid customer")
            continue
        if total_amount == 0:
            total_amount = 1
        invoice_payload = {
            "InvoiceCode": str(invoice.get("InvoiceID")),
            "Number": str(invoice.get("InvoiceNumber")),
            "CreatedDate": invoice.get("InvoiceDate"),
            "DueDate": invoice.get("DueDate"),
            "OriginalAmount": str(abs(total_amount)),
            "AmountOwing": amount_owing,
            "Customer": {
                "CustomerCode": customer_code,
            },
            "CustomFields": [
                {
                    # "Job Code": str(invoice.get("Job").get("JobCode")),
                    # "Job Description": str(invoice.get("Job").get("JobDescription")),
                    "Name": "Project Number", 
                    "Value": str(invoice.get("Job").get("JobCode")),
                },
                {
                    "Name": "Project Name",
                    "Value": str(invoice.get("Job").get("JobDescription") or "N/A"),
                },
                {
                    "Name": "Invoice Comment",
                    "Value": str(invoice.get("Comment") or "N/A") ,
                }
            ]
        }
        invoice_serializer_payload.append(
            {
                "id": invoice.get("InvoiceID"),
                "client_id": user_id,
                "client_code": customer_code,
                "customer_id": invoice.get("Client").get("ClientID"),
                "amount_owning": amount_owing,
                "amount_paid": amount_paid,
                "due_date": invoice.get("DueDate"),
                "created_at": invoice.get("InvoiceDate"),
                "is_paid": (invoice or {}).get("InvoicePaid", False),
                "is_synced": False,
            }
        )
        invoice_list.append(invoice_payload)
    return invoice_list, invoice_serializer_payload


def get_access_token(iodm_access_key, iodm_secret_key):
    url = f"{iodm_url}authorise/token"
    body = {"Key": iodm_access_key, "Token": iodm_secret_key}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    return data.get("AccessToken")


def save_customer(access_token, customers):
    # get length of customers and divide it by 99 to get the number of pages
    # then loop through the pages and save the customers
    customers_per_page = 90
    number_of_pages = len(customers) // customers_per_page
    for page in range(number_of_pages):
        start = page * customers_per_page
        end = (page + 1) * customers_per_page
        body = {"Customers": customers[start:end]}

        url = f"{iodm_url}customer"
        headers = {
            "Authorization": f"{access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print(response.json())  # print the response
            continue
        print("REsp", response)
        print("Customer not saved")


def save_invoice(access_token, invoices):
    invoices_per_page = 99

    number_of_pages = len(invoices) // invoices_per_page
    for page in range(number_of_pages):
        start = page * invoices_per_page
        end = (page + 1) * invoices_per_page
        body = {"Invoices": invoices[start:end]}
        url = f"{iodm_url}invoice"
        headers = {
            "Authorization": f"{access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print(response.json())  # print the response
        else:
            print("REsp", response.json())
            print("invoice")
            print("Invoice not saved")


def save_data_to_db(customers, invoices):
    for customer in customers:
        serializer = CustomerSerializer(data=customer)
        try:
            serializer.create_or_update(serializer.initial_data)
        except Exception as e:
            print(e, " customer errors")

    for invoice in invoices:
        serializer = InvoiceSerializer(data=invoice)
        try:
            serializer.create_or_update(serializer.initial_data)
        except Exception as e:
            print(e, " invoice errors")
    

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
    users = User.objects.filter(is_staff=False)

    for user in users:
        secret_key = user.abtract_secret_key
        all_clients = get_clients(secret_key)
        client_contacts = get_client_contacts(secret_key)
        clients_adress = get_client_adress(secret_key)
       
        # # print timestampe
        # print(timezone.now())
        # print("-=-------=-=-= client_contacts_done")
        customers, customer_serializer_payload = create_customer_payload(
            all_clients, client_contacts, clients_adress, user.id
        )
        
        print("-=-------=-=-= customers_done")
        invoices = get_all_invoices(
            secret_key, user.abtract_start_page, user.abtract_page_size
        )
        print(timezone.now())
        print("-=-------=-=-= invoices_done")
        invoices, invoice_serializer_payload = create_invoice_payload(user.id, invoices, all_clients)
        print(timezone.now())
        # write invoices to a text file

        print("-=-------=-=-= invoices_payload_done")
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
        save_customer(access_token, customers)
        print(timezone.now())
        print("-=-------=-=-= save_customer_done")
        print("invoices length", len(invoices))
        save_invoice(access_token, invoices)
        print(timezone.now())
        customers = Customer.objects.filter(is_synced=False)
        invoices = Invoice.objects.filter(is_synced=False)
        update_data_synced(customers, invoices)
        print(timezone.now())
        print("-=-------=-=-= update_data_synced_done")
        print("Data Synced")
