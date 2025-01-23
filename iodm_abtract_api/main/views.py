from django.shortcuts import render
from .utils.utils import main
from .utils.email_fetcher import check_emails

# Create your views here.
# create a simple view which when runned will run main in utils and save data to db


def run_main(request):
    main()
    return render(request, "main.html")


def check_emails_view(request):
    check_emails()
    return render(request, "main.html")

