from django.contrib.flatpages.views import flatpage
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", flatpage, {"url": "/about-us/"}, name="about"),
    # path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path(
        "muzamil",
        views.me,
    ),
]
