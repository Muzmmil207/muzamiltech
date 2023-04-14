from django.shortcuts import get_object_or_404, render

from .models import Article


def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {"article": article}
    return render(request, "apps/articles/article.html", context=context)
