from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.articles.models import Article
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .serializers import ArticlesSerializer


@api_view(["GET"])
def get_routes(request, format=None):

    return Response(
        {
            "all user Articles": reverse("Articles_list", request=request, format=format),
        }
    )


class ArticlesList(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = ArticlesSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "content"]

    # With cookie: cache requested url for each user for 2 minute
    # @method_decorator(cache_page(60 * 2))
    # @method_decorator(vary_on_cookie)
    def get(self, request, format=None):
        return self.list(request)

    def get_queryset(self):
        queryset = Article.objects.all().order_by("-published_at", "title")
        return queryset
