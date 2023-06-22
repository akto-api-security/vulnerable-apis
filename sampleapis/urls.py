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
    path("profile/edit-details/upload-transcript/", views.upload_transcript, name="upload_transcript"), #SSRF on CSV upload
    path("profile/edit-details/upload-profile-image/", views.upload_profile_pic, name="upload_profile_pic"), #SSRF on Image upload
    path("profile/edit-details/upload-resume/", views.upload_resume, name="upload_resume"), #SSRF on PDF upload
    path("academics/curriculum/upload-lab-reports/", views.upload_lab_report, name="upload_lab_report"), #SSRF on XML upload
    path("home/search/", views.search_portal, name="search_website"), #SSRF on AWS Meta Endpoint
    path("home/recents/", views.getRecents, name="recents"), #SSRF on Localhost
    path("home/tnp-notifications/view/", views.getTnp_notifications, name="tnp_notifications"), #SSRF on Lcalhost DNS Pinning
    path("profile/documents/view/", views.getDocuments, name="view_documents"), #SSRF on Files
]

