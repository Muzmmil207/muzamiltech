from django.contrib.flatpages.views import flatpage
from django.urls import include, path

from . import views

urlpatterns = [
    path("<slug:slug>", views.article, name="article"),
]
