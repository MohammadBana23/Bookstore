import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from bookstore.api.tools.api import CustomException
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from datetime import date
from . import Book

class UserManager(BaseUserManager):
    """
    Custom user model manager where email or phone is the unique
    identifiers for authentication instead of usernames.
    """

    def create_user(
        self, email, phone, password, username=None, **extra_fields
    ):
        """
        Create and save a user with the given email and password.
        """

        # set is_active to True so we can authenticate this user later
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_active") is not True:
            raise ValueError()

        # we need to generate a unique username as identifier
        username = generate_username(username)
        if not password:
            raise CustomException(
                "لطفا رمزعبور را وارد کنید.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, username=username, **extra_fields)
            user.set_password(password)
            user.save()
            return user

        elif phone:
            user = self.model(phone=phone, username=username, **extra_fields)
            user.set_password(password)
            user.save()
            return user

        else:
            raise CustomException(
                "لطفا ایمیل یا شماره تلفن خود را وارد کنید.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def create_superuser(self, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError()
        if extra_fields.get("is_superuser") is not True:
            raise ValueError()
        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    cash = models.IntegerField(default=0)
    books = models.ManyToManyField(Book)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    def __str__(self):
        return f"user obj: {self.email} - {self.phone}"
    
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


def generate_username(value):
    """
    we have to generate username so create_superuser
    method does not get in trouble, this function will
    get phone or email and return username
    """
    if value is None:
        """this method is called by api"""
        # we need to generate unique username
        # for each user, so we use uuid
        # for this purpose
        uuid_tmp = str(uuid.uuid4())
        x = uuid_tmp.split("-")
        id = random.choice(x)

        username = "goodoperuser-" + id
        return username

    else:
        """this method is called by django create_superuser"""
        # checking if the username if unique
        if User.objects.filter(username=value).exists():
            # this username is already taken
            raise CustomException(
                "کاربری با این اطلاعات وجود دارد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return value
