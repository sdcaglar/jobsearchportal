from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None):
        user = self.create_user(
            email,
            name=name,
            surname=surname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = PhoneNumberField(null=True, blank=True)
    identity_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Job(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    company = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    publishing_date = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("job-detail", kwargs={"pk": self.pk})


class UserJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="x")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="y")
    date = models.DateTimeField(default=timezone.now)
    evaluation_result = models.TextField()
