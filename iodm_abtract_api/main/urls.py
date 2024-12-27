from django.contrib import admin
from django.urls import path

from main.views import run_main

urlpatterns = [
    path("run_main/", run_main, name="run_main"),
]
