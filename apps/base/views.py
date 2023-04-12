from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "apps/base/home.html")


def about(request):
    return render(request, "apps/base/about.html")


def contact(request):
    return render(request, "apps/base/contact.html")
