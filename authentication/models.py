# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'User'),
    )
    email = models.EmailField('email address', unique=True) # changes email to unique and blank to false
    email_verified = models.BooleanField(default=False)
    forget_password_token = models.TextField(null=True, blank=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email
