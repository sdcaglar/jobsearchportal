from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    create_jobseeker,
    create_recruiter,
    login_jobseeker,
    login_recruiter,
    logout_jobseeker,
    logout_recruiter,
    HomeView,
    UserHomeView,
    change_password,
    JobDetailView,
    JobEditView,
    JobDeleteView,
    create_job,
    apply_job,
    JobEvaluationDetailView,
    SearchView,
    profile,
    jobseeker_profile,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("jobseeker/login/", login_jobseeker, name="jobseeker-login"),
    path("jobseeker/logout/", logout_jobseeker, name="jobseeker-logout"),
    path("jobseeker/signup/", create_jobseeker, name="jobseeker-signup"),
    path("recruiter/login/", login_recruiter, name="recruiter-login"),
    path("recruiter/logout/", logout_recruiter, name="recruiter-logout"),
    path("recruiter/signup/", create_recruiter, name="recruiter-signup"),
    path("home", login_required(UserHomeView.as_view()), name="user-home"),
    path("profile", profile, name="profile"),
    path("jobseeker-profile/<int:pk>/", jobseeker_profile, name="jobseeker-profile"),
    path("settings/", change_password, name="settings"),
    path("job/<int:pk>/", login_required(JobDetailView.as_view()), name="job-detail"),
    path("job/<int:pk>/edit", login_required(JobEditView.as_view()), name="edit-job"),
    path(
        "job/<int:pk>/delete",
        login_required(JobDeleteView.as_view()),
        name="delete-job",
    ),
    path("job/create/", create_job, name="create-job"),
    path("job/<int:pk>/apply", apply_job, name="apply-job"),
    path(
        "job/evaluation/<int:pk>",
        login_required(JobEvaluationDetailView.as_view()),
        name="evaluation-job",
    ),
    path("search", SearchView.as_view(), name="search-jobs"),
]
