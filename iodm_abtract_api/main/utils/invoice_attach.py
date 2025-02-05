import requests

def get_invoice(invoice_number, access_token):
    query = "query GET_INVOICES_FOR_COMPANY( \
    $InvoiceState: String \
    $InvoiceNumber: String \
    $Customer: String \
    $CustomerCode: String \
    $CreatedDateMin: String \
    $CreatedDateMax: String \
    $DueDateMin: String \
    $DueDateMax: String \
    $AmountType: String \
    $AmountValue: String \
    $AmountOperator: String \
    $SortField: String \
    $Ascending: Boolean \
    $PageSize: Int \
    $Skip: Int \
    $InvoiceIds: [ID] \
    $CustomFieldFilters: String \
    $CustomFieldSort: String \
) { \
    GetInvoicesForCompany( \
            Filter: { \
                InvoiceState: $InvoiceState \
                InvoiceNumber: $InvoiceNumber \
                Customer: $Customer \
                CustomerCode: $CustomerCode \
                CreatedDateMin: $CreatedDateMin \
                CreatedDateMax: $CreatedDateMax \
                DueDateMin: $DueDateMin \
                DueDateMax: $DueDateMax \
                AmountType: $AmountType \
                AmountValue: $AmountValue \
                AmountOperator: $AmountOperator \
                SortField: $SortField \
                Ascending: $Ascending \
                PageSize: $PageSize \
                Skip: $Skip \
                InvoiceIds: $InvoiceIds \
                CustomFieldFilters: $CustomFieldFilters \
                CustomFieldSort: $CustomFieldSort             \
            } \
        ) { \
            Invoices { \
                Id \
                InvoiceCode \
                Number \
                CreatedDate \
                LocalCreatedDate \
                DueDate \
                LocalDueDate \
                OriginalAmount \
                AmountOwing \
                State \
                SettledDate \
                LocalSettledDate \
                Customer { \
                    CustomerCode \
                    CompanyName \
                    DisplayName \
                    Contacts { \
                        Id \
                        FirstName \
                        LastName \
                        AddressLine1 \
                        AddressLine2 \
                        City \
                        State \
                        Postcode \
                        Country \
                        Email \
                        MobileNumber \
                    } \
                } \
                Tickets { \
                    Id \
                    CompanyId \
                    TicketNumber \
                    State \
                    Details \
                    ResolvedReason \
                    ResolvedDateTime \
                    CreatedDateTime \
                    TicketOption { \
                        Id \
                        Reason \
                        CaptureMessage \
                        Type \
                    } \
                    Uri \
                } \
                Uri \
                CustomFields { \
                    Name \
                    Value \
                } \
                Attachments { \
                    FileId \
                    IsPublic \
                    Title \
                } \
            } \
        } \
    }" 
    url = "https://api.sandbox.iodmconnectonline.com/graphql"
    body = {
        "query": query,
        "variables": {
            "InvoiceNumber":invoice_number,
            "Customer":"",
            "CustomerCode":"",
            "CreatedDateMin":"",
            "CreatedDateMax":"",
            "DueDateMin":"",
            "DueDateMax":"",
            "AmountType":"",
            "AmountValue":"",
            "AmountOperator":"",
            "InvoiceState":"All",
            "SortField":"Company name",
            "Ascending":"true",
            "PageSize":20,
            "Skip":0
        },
    }
    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json()["data"]["GetInvoicesForCompany"]["Invoices"][0]["Uri"]

def get_invoice_attachment_url(uri, access_token, filename):
    url = "https://api.sandbox.iodmconnectonline.com/document/attachtoresource"
    body = {
    "IsPublic": "true",
    "Title": filename,
    "FileName": filename,
    "Resource": {
        "Uri": uri
    }
    }
    headers = {
    "Authorization": f"{access_token}",
    "Content-Type": "application/json"

    }
    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json()["AttachmentUrl"]
   

def upload_invoice_attachment(file_path, attachment_url, access_token):
    url = attachment_url
    headers = {
    'Content-Type': 'application/pdf'
    # 'Authorization': f"{access_token}"
    }
    try:
        with open(file_path, "rb") as file:
            print("S")

            files = {"file": (file_path, file, "application/octet-stream")}
            print(file)
            #convert file to json
            response = requests.put(url, data=file)
            # print("Response:", response.json())
            # print("Status Code:", response.status_code)
            print("Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")

def attach_invoice(invoice_number, file_path, access_token,filename):
    uri = get_invoice(invoice_number, access_token)
    attachment_url = get_invoice_attachment_url(uri, access_token, filename)
    upload_invoice_attachment(file_path, attachment_url, access_token)

