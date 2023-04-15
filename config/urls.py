from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("articles/", include("apps.articles.urls")),
    path("api/", include("apps.api.urls")),
    path("", include("apps.base.urls")),
]
