from django.http import JsonResponse
from django.shortcuts import render


def home(request):

    return render(request, "apps/base/home.html")
