from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.user_signUp, name="signup"),
    path("login/", views.user_signIn, name="login"),
    path("home/", views.echo, name="home"),
    path("profile/view-details/", views.getUserProfile , name="user_profile"), #TRACE Vulnerability
    path("dashboard/notice/", views.getNotices, name="dashboard"), #TRACK Vulnerability
    path("academics/results/", views.getResults, name="academics"), #Server Version Disclosure
    path("feedback/", views.getFeedbacks, name="feedback"), #Open Redirect Vulnerability also OPEN_REDIRECT_SUBDOMAIN_WHITELIST
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
    path("settings/<int:user_id>/update-email/", views.update_email, name='update_email'),
    path("settings/<int:user_id>/update-phone-number/", views.update_phone_number, name='update_phone_number'),
    path("settings/<int:user_id>/change-username/", views.change_username, name="change_username"),
    path("settings/<int:user_id>/update-profile-details/", views.edit_user_profile, name="update_profile"),
    path('settings/payments/<int:user_id>/add-card/', views.add_card, name='add_card'),
    path('settings/payments/<str:user_id>/card-details/', views.get_card_details, name='get_card_details'), #SQL injection
    path("academics/e-library/", views.open_library, name="open_e-library"), #OPEN_REDIRECT_HOST_HEADER_INJECTION
    re_path(r'^blogs/view/(?P<url>.+)$', views.view_blog, name='view_blog'), #OPEN_REDIRECT_IN_PATH
    path("settings/<int:user_id>/delete-account/", views.delete_user, name="delete_account"),
    path("dashboard/add-student/",views.add_student, name="add_student"),
    path("students/result/add-result/", views.add_result, name="add_result"),
    path("students/search/", views.get_student, name="get_student"), #noSQL injection
]

