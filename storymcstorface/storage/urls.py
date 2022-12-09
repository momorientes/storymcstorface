from django.urls import include, path
from storage import views

urlpatterns = [
    path("", views.facility_list, name="facility_list"),
    path("select2/", include("django_select2.urls")),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("<str:slug>/", views.facility_detail, name="facility_detail"),
    path("<str:slug>/modify/", views.facility_modify, name="facility_modify"),
]
