import json

import requests

from apps.articles.models import Article
from apps.base.forms import ContactForm
from apps.devices.models import Brand, Device
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Contact, NewsletterSubscriber


def home(request):
    articles = Article.objects.order_by("-published_at").exclude(image_url=None)[:6]
    brands = Brand.objects.all()
    devices = Device.objects.all()
    context = {"articles": articles, "brands": brands, "devices": devices}
    return render(request, "apps/base/home.html", context=context)


def about(request):
    return render(request, "apps/base/about.html")


def contact(request):
    return render(request, "apps/base/contact.html")


@require_http_methods(["POST"])
def contact_handler(request):
    data = json.loads(request.body)
    contact_data = ContactForm(data=data)

    if contact_data.is_valid():
        contact_data.save()
        return JsonResponse("Thanks for reaching out! we'll be in touch soon.", safe=False)
    return JsonResponse(
        "{1} <br> <a href='{0}'>try again</a>.".format(
            reverse("contact"),
            contact_data.errors,
        ),
        safe=False,
    )


@require_http_methods(["POST"])
def subscribe_handler(request):
    data = json.loads(request.body)
    try:
        subscribe = NewsletterSubscriber(
            email=data["email"],
        )
        subscribe.save()
        return JsonResponse("Thanks :)", safe=False)
    except Exception as e:
        return JsonResponse("Some thing want wrong :(", safe=False)
