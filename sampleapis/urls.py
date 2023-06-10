from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("echo/", views.echo, name="echo"),
    path("track/", views.track, name="track"),
    path("serverversion/", views.serverversion, name="serverversion"),
]

