from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import JobSeekerSignUpForm, RecruiterSignUpForm, JobForm
from .models import Job, UserJob, User
from .admin import UserChangeForm
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = "base.html"


class UserHomeView(ListView):
    model = Job
    template_name = "user_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_recruiter:
            context["jobs"] = Job.objects.filter(publisher=self.request.user)
        if self.request.user.is_jobseeker:
            if "search_job" in self.request.GET:
                table_search = self.request.GET.get("table_search")
                context["jobs"] = Job.objects.filter(Q(name__icontains=table_search))
            else:
                context["jobs"] = Job.objects.all()
            context["my_jobs"] = UserJob.objects.filter(user=self.request.user)
        return context


class UserProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = "profile.html"
    fields = [
        "name",
        "surname",
        "email",
        "profile_image",
        "phone",
        "identity_number",
        "address",
    ]
    success_message = "Successfully updated"
    error_message = "Oops, Information could not be updated"


class JobDetailView(DetailView):
    model = Job
    template_name = "detail_job.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = Job.objects.filter(pk=self.kwargs.get("pk"))
        if self.request.user.is_recruiter:
            context["applications"] = UserJob.objects.filter(job=self.kwargs.get("pk"))
        return context


class JobEvaluationDetailView(DetailView):
    model = UserJob
    template_name = "evaluation_job.html"


class JobEditView(SuccessMessageMixin, UpdateView):
    model = Job
    template_name = "edit_job.html"
    fields = ["name", "details"]
    success_message = "Successfully updated"
    error_message = "Oops, Information could not be updated"


class JobDeleteView(SuccessMessageMixin, DeleteView):
    model = Job
    template_name = "delete_job.html"
    fields = ["name"]
    success_url = reverse_lazy("user-home")
    success_message = "The created job posting has been deleted"
    error_message = "Oops, this job could not be deleted"


class SearchView(ListView):
    model = Job
    template_name = "base.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        jobs = {}
        if search is not None:
            jobs = Job.objects.filter(
                Q(name__icontains=search) | Q(company__icontains=search)
            )
        return jobs


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST.get("new_password1"))
            if user.is_recruiter:
                return redirect("recruiter-login")
            else:
                return redirect("jobseeker-login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "settings.html", {"form": form})


def create_jobseeker(request):
    if request.method == "POST":
        jobseeker_form = JobSeekerSignUpForm(request.POST)
        if jobseeker_form.is_valid():
            jobseeker = jobseeker_form.save(commit=False)
            jobseeker.save()
            messages.success(request, "Account was created")
            return redirect("jobseeker-login")
        else:
            messages.error(request, "Oops, this account could not be created")
    else:
        jobseeker_form = JobSeekerSignUpForm()
    return render(
        request, "accounts/jobseeker/signup.html", {"jobseeker_form": jobseeker_form}
    )


def login_jobseeker(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None and user.is_jobseeker:
            login(request, user)
            return redirect("user-home")
        else:
            messages.error(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/jobseeker/login.html", context)


@login_required
def logout_jobseeker(request):
    logout(request)
    return redirect("home")


def create_recruiter(request):
    if request.method == "POST":
        recruiter_form = RecruiterSignUpForm(request.POST)
        if recruiter_form.is_valid():
            jobseeker = recruiter_form.save(commit=False)
            jobseeker.save()
            messages.success(request, "account was created")
            return redirect("recruiter-login")
        else:
            messages.error(request, "Oops, this account could not be created")
    else:
        recruiter_form = RecruiterSignUpForm()
    return render(
        request, "accounts/recruiter/signup.html", {"recruiter_form": recruiter_form}
    )


def login_recruiter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None and user.is_recruiter:
            login(request, user)
            return redirect("user-home")
        else:
            messages.error(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/recruiter/login.html", context)


@login_required
def logout_recruiter(request):
    logout(request)
    return redirect("home")


@login_required
def create_job(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.publisher = request.user
            job.save()
            messages.success(request, "Your job posting has been successfully created.")
            return redirect("user-home")
    else:
        job_form = JobForm()
    return render(request, "create_job.html", {"job_form": job_form})


@login_required
def apply_job(request, pk):
    user = request.user
    job = get_object_or_404(Job, pk=pk)
    if request.method == "POST":
        if UserJob.objects.filter(user=user, job=job).exists():
            messages.error(request, "You have already applied for this posting.")
            return render(request, "apply_job.html", {"job": job})
        else:
            UserJob.objects.create(user=user, job=job)
            messages.success(
                request, "Your application for the job has been successfully completed"
            )
            return redirect("user-home")
    else:
        return render(request, "apply_job.html", {"job": job})


@login_required
def profile(request):
    user = request.user
    form = UserChangeForm(instance=user)
    if request.method == "POST":
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "profile.html", context)


@login_required
def jobseeker_profile(request, pk):
    user = get_object_or_404(User, pk=pk)

    return render(request, "jobseeker_profile.html", {"jobseeker": user})


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})
