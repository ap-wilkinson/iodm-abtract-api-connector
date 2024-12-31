import requests

# Variables
# Replace with your URL
access_token = "eyJraWQiOiJmeVwvU3l5QnNGWlwvdVwvempCbUx4MWJlM296T1BGVFlKNnM1RHFGMFBuYkkwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjZTVkMmY1My0zMzNhLTQ3ODctOTJkYy0wZGYzMWFkYzQ0MjYiLCJldmVudF9pZCI6IjM3ZmFlYWQ2LTcwOWEtNDEzNy1iMjU5LTA3ZmFlMGUxYjljYSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MzQzODQ2OTgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMi5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMl9yWUpEQ0RDeVIiLCJleHAiOjE3MzQzODgyOTgsImlhdCI6MTczNDM4NDY5OCwianRpIjoiN2Y0OWRiNjktYTk2YS00MDViLTg2MTUtNTZhMGRjMTE1ODIyIiwiY2xpZW50X2lkIjoiNG9uYjY1cDZjdGplMDM2Y2ZnNmEyYnI1Y2siLCJ1c2VybmFtZSI6ImxDQW1pVlFvckh6UVNUd1p0MnhtSk5YOWZBVXZ1WVpLOXY1YVE2bGxKZDQ9In0.HW9Ie6ik-czigz-X__Ha4IHKQF0mJcL18V_fDoRsRwg5GhDi_MPj-TRFPuiDGC5KbwkoPEDOiWMXvXKqxKtOQPpdp1bs_jothPmcCEvmMRqdW_jVA9XuofsjdLfMoq0jqpsKkX6WgRmsOOqFNW5aeKF7NmTwlgRNm6Ybab9l6X1nDmODoZtmIyN1mm9G-DrnRNG8xBbD1RscqKUUXlHFr31JF8gesiHhVccGpHNXD2BHIo36Yad7k900p6j1OhRciQ1Trr1sxQLrpWh-xthtIUpGpfOhq89vi7T1fFI_sHRhPlz4Yzz9y5LXJHCCixlgsyaDfl3HbZc3vCrhX7jmAQ"  # Replace with your access token
# api_token = ""

# Headers
headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}


def get_access_token():
    url = "https://api.sandbox.iodmconnectonline.com/authorise/token"
    body = {
        "Key": "b7+EThXa49vAIU7/5GCOROfJjXcDnEW+DoqOPtQmBqU=",
        "Token": "qMssu6Bc6+pmGX8RaLqsXgVghchgNMzrz2Av89oMYuE=",
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    global access_token
    access_token = response.json()["AccessToken"]
    print("Access Token:", access_token)


# Make the request
def get_cutomers_for_company():
    query = "query GET_CUSTOMERS_FOR_COMPANY(\
    $Customer: String\
    $InclusiveContact: Boolean\
    $Contact: Int\
    $ATBType: Int\
    $AmountType: String\
    $AmountValue: String\
    $AmountOperator: String\
    $SortField: String\
    $Ascending: Boolean\
    $PageSize: Int\
    $Skip: Int\
    $CustomFieldFilters: String\
    $CustomFieldSort: String\) {\
    GetCustomersForCompany(\
        Filter: {\
            Customer: $Customer\
            InclusiveContact: $InclusiveContact\
            Contact: $Contact\
            ATBType: $ATBType\
            AmountType: $AmountType\
            AmountValue: $AmountValue\
            AmountOperator: $AmountOperator\
            SortField: $SortField\
            Ascending: $Ascending\
            PageSize: $PageSize\
            Skip: $Skip\
            CustomFieldFilters: $CustomFieldFilters\
            CustomFieldSort: $CustomFieldSort\
        }\
    ) {\
        Customers {\
            Id\
            CustomerCode\
            CompanyName\
            IsVip\
            DisplayName\
            Contacts {\
                Id\
                FirstName\
                LastName\
                AddressLine1\
                AddressLine2\
                City\
                State\
                Postcode\
                Country\
                Email\
                MobileNumber\
            }\
             TaxNumber\
            SecondaryTaxNumber\
            Uri\
            TicketCount\
            CustomFields {\
                Name\
                Value\
            }\
            Attachments {\
                FileId\
                IsPublic\
                Title\
            }\
        }\
    }\
}\
   "  # Replace with your query parameters
    body = {
        "query": query,
        "variables": {
            "Customer": "",
            "InclusiveContact": "true",
            "Contact": 0,
            "AmountType": "",
            "AmountValue": "",
            "AmountOperator": "",
            "SortField": "Company name",
            "Ascending": "true",
            "PageSize": 20,
            "Skip": 0,
        },
    }  # Replace with your body content
    url = "https://api.sandbox.iodmconnectonline.com/graphql"
    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


def save_customer():
    body = {
        "CustomerId": "703059",
        "Customers": [
            {
                "CustomerCode": "703059",
                "CompanyName": "Testing tProperty Industrial Constructions Pty Ltd",
                "DisplayName": "Testing tProperty Industrial Constructions Pty Ltd",
                "TaxNumber": "",
                "SecondaryTaxNumber": "",
                "IsVip": "false",
                "Contacts": [
                    {
                        "FirstName": "Antony McLandsborough",
                        "LastName": "",
                        "AddressLine1": "Level 2",
                        "AddressLine2": "1C Homebush Bay Drive",
                        "City": "Rhodes NSW 2138",
                        "State": "",
                        "Postcode": "",
                        "Country": "AU",  # might need to hard code in
                        "Email": "emily.bladen@frasersproperty.com.au",
                        "MobileNumber": "",
                        "PhoneNumber": "",
                    }
                ],
            }
        ],
    }
    url = "https://api.sandbox.iodmconnectonline.com/customer"
    print("_----------------------- \n Access tojen", access_token)

    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response)


def save_invoice():
    body = {
        "Invoices": [
            {
                "InvoiceCode": "16699",
                "Number": "16699",
                "CreatedDate": "2014-11-30T00:00:00",
                "DueDate": "2014-12-29T00:00:00",
                "OriginalAmount": "895",
                "AmountOwing": "0",
                "Customer": {
                    "CustomerCode": "832589",
                },
            }
        ]
    }
    url = "https://api.sandbox.iodmconnectonline.com/invoice"
    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=body)
    print("Status Code:", response.status_code)
    print("Response:", response.json())


get_access_token()
# # get_cutomers_for_company()
# save_customer()
save_invoice()
