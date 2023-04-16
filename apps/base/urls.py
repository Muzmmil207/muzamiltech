from django.contrib.flatpages.views import flatpage
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", flatpage, {"url": "/about-us/"}, name="about"),
    # path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("contact-handler", views.contact_handler),
    path("subscribe-handler", views.subscribe_handler),
    path(
        "muzamil",
        views.me,
    ),
]
