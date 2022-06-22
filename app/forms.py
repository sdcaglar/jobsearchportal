from django.forms import ModelForm
from .admin import UserCreationForm
from .models import User, Job


class JobSeekerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_jobseeker = True

        if commit:
            user.save()
        return user


class RecruiterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        if commit:
            user.save()
        return user


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ["name", "details", "company", "company_address"]
