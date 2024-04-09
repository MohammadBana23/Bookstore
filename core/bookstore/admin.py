from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from bookstore.models import User, Book, BuyBook


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "phone",
        "username",
        "birthdate",
        "cash",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "is_special",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "is_special")
    search_fields = ("email", "phone", "username")
    ordering = ("created_at", "updated_at", "id")
    fieldsets = (
        ("Authentication", {"fields": ("email", "phone", "username", "password" , "birthdate")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
    )
    add_fieldsets = (
        (
            "Registration",
            {
                "classes": ("wide",),
                "fields": ("username", "phone", "email", "password1", "password2"),
            },
        ),
    )
    
class BookAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        "id",
        "name",
        "author",
        "publisher",
        "get_categories",
        "cost",
        "link_download",
        "language",
        "year",
        "pages_num",
        "is_special",
        "created_at",
        "updated_at",
    )
    list_filter = ("year", "is_special")
    search_fields = ("name", "cost", "language")
    ordering = ("created_at", "updated_at", "id")

class BuyBookAdmin(admin.ModelAdmin):
    model = BuyBook
    list_display = (
        "user",
        "book",
        "created_at",
        "updated_at",
    )
    search_fields = ("user", "book")
    ordering = ("created_at", "updated_at", "id")
    

admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BuyBook, BuyBookAdmin)