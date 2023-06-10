from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("echo/", views.echo, name="echo"),
    path("trace/", views.trace_method_test, name="trace_method_test"),
    path("track/", views.track_method_test, name="track_method_test"),
    path("serverversion/", views.server_version_disclosure_test, name="server_version_disclosure_test"),
]

