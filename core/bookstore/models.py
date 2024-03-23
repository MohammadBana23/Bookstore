from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from . import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    cash = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def age(self):
        today = date.today()
        if self.birthdate != None:
            age = (
                today.year
                - self.birthdate.year
                - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            )
            return age
