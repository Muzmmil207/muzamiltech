from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_user, name="login"),
    path("muzamil", views.me, name="me"),
]
