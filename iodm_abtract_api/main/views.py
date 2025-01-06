from django.shortcuts import render
from .utils import main

# Create your views here.
# create a simple view which when runned will run main in utils and save data to db


def run_main(request):
    main()
    return render(request, "main.html")



