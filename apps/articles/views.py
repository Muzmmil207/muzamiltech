from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from utils.functional import get_url

from .models import Article


def articles(request):
    context = {"articles": "s"}
    return render(request, "apps/articles/articles.html", context=context)


def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    con = article.content
    article.content = "".join([f"<p>{i}</p>" for i in con.split(". ")])
    article.save()
    article_id = article.id
    next_prev_articles = Article.objects.filter(id__in=[article_id + 1, article_id - 1]).values(
        "title", "slug"
    )
    url = get_url(request)
    context = {
        "article": article,
        "next_prev_articles": next_prev_articles,
        "url": url,
    }
    return render(request, "apps/articles/article.html", context=context)
