from django.contrib.flatpages.views import flatpage
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views
from .sitemaps import ArticleSitemap

sitemaps = {"articles": ArticleSitemap}

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", flatpage, {"url": "/about-us/"}, name="about"),
    # path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("contact-handler", views.contact_handler),
    path("subscribe-handler", views.subscribe_handler),
    # Search engine crawlers stuff
    path(
        "sitemaps.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"),
    ),
]
