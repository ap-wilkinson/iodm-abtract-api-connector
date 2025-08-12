from django.contrib import admin
from django.urls import path

from main.views import run_main, check_emails_view

urlpatterns = [
    path("run_main/", run_main, name="run_main"),
    path('', run_main, name="index"),
    path('emails/', check_emails_view, name="check_emails"),
]
