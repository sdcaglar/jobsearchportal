from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import JobSeekerSignUpForm, RecruiterSignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class HomeView(TemplateView):
    template_name = "base.html"


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
