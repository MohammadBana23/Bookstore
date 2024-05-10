# Generated by Django 4.2 on 2024-05-10 19:41

import bookstore.models.buybook
import bookstore.models.token
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("birthdate", models.DateField(blank=True, null=True)),
                ("cash", models.IntegerField(default=0)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_special", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                ("publisher", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to="book-images/"),
                ),
                (
                    "book_file",
                    models.FileField(blank=True, null=True, upload_to="books/"),
                ),
                (
                    "link_download",
                    models.CharField(blank=True, max_length=1023, null=True),
                ),
                (
                    "link_download_10pages",
                    models.CharField(blank=True, max_length=1023, null=True),
                ),
                ("cost", models.IntegerField(default=0)),
                (
                    "language",
                    models.CharField(
                        choices=[("ENGLISH", "English"), ("PERSIAN", "Persian")],
                        default="ENGLISH",
                        max_length=255,
                    ),
                ),
                ("year", models.IntegerField(blank=True, null=True)),
                ("pages_num", models.IntegerField(blank=True, default=0, null=True)),
                ("is_special", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="VerificationToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "receiver",
                    models.CharField(
                        max_length=64, unique=True, verbose_name="Receiver"
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        default=bookstore.models.token.create_random_token,
                        max_length=6,
                        verbose_name="Token",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "expired_at",
                    models.DateTimeField(
                        default=bookstore.models.token.calculate_expiration_datetime
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BuyBook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "expired_at",
                    models.DateTimeField(
                        default=bookstore.models.buybook.calculate_expiration_datetime
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="bookstore.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
        migrations.AddField(
            model_name="book",
            name="categories",
            field=models.ManyToManyField(to="bookstore.category"),
        ),
        migrations.AddField(
            model_name="user",
            name="books",
            field=models.ManyToManyField(to="bookstore.book"),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
