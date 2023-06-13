from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.echo, name="home"),
    path("profile/view-details/", views.getUserProfile , name="user_profile"), #TRACE Vulnerability
    path("dashboard/notice/", views.getNotices, name="dashboard"), #TRACK Vulnerability
    path("academics/results/", views.getResults, name="academics"), #Server Version Disclosure
    path("feedback/", views.getFeedbacks, name="feedback"), #Open Redirect Vulnerability
    path("academics/courses/", views.getCourseList, name="courses"), #Page Dos Vulnerability
    path("academics/courses/v1/registration/payment/", views.payment_v1, name="registration"),
    path("academics/courses/v2/registration/payment/", views.payment_v2, name="registration"), #Old Api Version Vulnerability
    path("dashboard/attendence/", views.getAttendence, name="profile-details"), #Content Type Header Missing Vulnerability
]

