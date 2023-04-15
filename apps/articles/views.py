from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from .models import Article


def articles(request):
    context = {"articles": 's'}
    return render(request, "apps/articles/articles.html", context=context)

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {"article": article}
    return render(request, "apps/articles/article.html", context=context)

def get_article(request):
    search_query = request.GET.get('search-articles','')
    articles = Article.objects.filter
    return JsonResponse()