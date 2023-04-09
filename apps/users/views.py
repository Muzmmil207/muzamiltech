from django.http import JsonResponse
from django.shortcuts import render


def login_view(request):

    return render(request, "apps/users/login.html")
