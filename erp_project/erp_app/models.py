from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.db import models

# Custom manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.full_name or self.email


# Workspace (like a team/organization)
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Membership (connects User to Workspace with a role)
class Membership(models.Model):
    ROLE_CHOICES = [
        ("OWNER", "Owner"),
        ("MEMBER", "Member"),
        ("GUEST", "Guest"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="MEMBER")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "workspace")  # a user can only join once

    def __str__(self):
        return f"{self.user.email} in {self.workspace.name} as {self.role}"