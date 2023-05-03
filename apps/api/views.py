from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.articles.models import Article
from apps.devices.models import Device
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .serializers import ArticlesSerializer, DevicesSerializer


@api_view(["GET"])
def get_routes(request, format=None):

    return Response(
        {
            "all user Articles": reverse("articles-api", request=request, format=format),
        }
    )


######################
# Articles App Views #
######################


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


####################
# Device App Views #
####################
class DevicesList(generics.ListAPIView):

    serializer_class = DevicesSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ["title", "content"]
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Device.objects.exclude(status="new inserted").order_by("?")
        return queryset
