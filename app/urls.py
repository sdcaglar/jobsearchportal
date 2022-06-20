from django.urls import path
from .views import (
    create_jobseeker,
    create_recruiter,
    login_jobseeker,
    login_recruiter,
    logout_jobseeker,
    logout_recruiter,
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("jobseeker/login/", login_jobseeker, name="jobseeker-login"),
    path("jobseeker/logout/", logout_jobseeker, name="jobseeker-logout"),
    path("jobseeker/signup/", create_jobseeker, name="jobseeker-signup"),
    path("recruiter/login/", login_recruiter, name="recruiter-login"),
    path("recruiter/logout/", logout_recruiter, name="recruiter-logout"),
    path("recruiter/signup/", create_recruiter, name="recruiter-signup"),
]
