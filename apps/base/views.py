import json

from apps.articles.models import Article
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Contact, NewsletterSubscriber


def home(request):
    articles = Article.objects.exclude(image_url=None).order_by("?")[:4]
    context = {"articles": articles}
    return render(request, "apps/base/home.html", context=context)


def about(request):
    return render(request, "apps/base/about.html")


def contact(request):
    return render(request, "apps/base/contact.html")


@require_http_methods(["POST"])
def contact_handler(request):
    data = json.loads(request.body)
    try:
        contact = Contact.objects.create(
            name=data["name"],
            email=data["email"],
            message=data["message"],
        )
        contact.save()
        return JsonResponse("Thanks for reaching out! we'll be in touch soon.", safe=False)
    except Exception as e:
        print(e)
        return JsonResponse("Some thing want wrong :(", safe=False)


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
