from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView
from .forms import JobSeekerSignUpForm, RecruiterSignUpForm
from .models import Job, UserJob, User


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
            context["jobs"] = Job.objects.all()
            context["my_jobs"] = UserJob.objects.filter(user=self.request.user)
        return context


class UserProfileView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = "profile.html"
    fields = ["name", "surname", "email", "phone", "identity_number", "address"]
    success_message = "Successfully updated"
    error_message = "Oops, Information could not be updated"


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
            messages.info(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/jobseeker/login.html", context)


def logout_jobseeker(request):
    logout(request)
    return redirect("home")


def create_recruiter(request):
    if request.method == "POST":
        recruiter_form = RecruiterSignUpForm(request.POST)
        print(recruiter_form)
        if recruiter_form.is_valid():
            jobseeker = recruiter_form.save(commit=False)
            jobseeker.save()
            messages.success(request, "account was created")
            return redirect("recruiter-login")
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
            messages.info(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/recruiter/login.html", context)


def logout_recruiter(request):
    logout(request)
    return redirect("home")
