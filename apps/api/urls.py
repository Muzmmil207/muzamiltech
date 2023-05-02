from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_routes),
    path("articles-list", views.ArticlesList.as_view(), name="articles-api"),
    path("devices-list", views.DevicesList.as_view(), name="devices-api"),
]
