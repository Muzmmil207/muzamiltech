from apps.base.sitemaps import ArticleSitemap
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import TemplateView

sitemaps = {"articles": ArticleSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("articles/", include("apps.articles.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("devices/", include("apps.devices.urls")),
    path("api/", include("apps.api.urls")),
    path("", include("apps.base.urls")),
    # Search engine crawlers stuff
    path(
        "sitemaps.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="site/robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="site/sitemap.xml", content_type="application/xml"),
    ),
]
