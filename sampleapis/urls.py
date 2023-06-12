from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("echo/", views.echo, name="echo"),
    path("home/", views.trace_method_test, name="trace_method_test"),
    path("dashboard/", views.track_method_test, name="track_method_test"),
    path("dashboard/details/", views.server_version_disclosure_test, name="server_version_disclosure_test"),
    path("view/", views.open_redirect, name="open_redirect"),
    re_path(r"^view/$", views.open_redirect, name="open_redirect_"),
    path("resources/", views.page_dos_test, name="page_dos_test"),
    path("v1/lookup/", views.api_version_1, name="api_version_1"),
    path("v2/lookup/", views.api_version_2, name="api_version_2"),
    path("view-details/", views.content_type_header_missing_test, name="content_type_header_missing_test"),
]

