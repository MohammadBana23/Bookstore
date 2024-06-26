from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from bookstore.models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "phone",
        "username",
        "birthdate",
        "cash",
        "get_books_bought",
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
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified", "is_special")},
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
    
    def get_books_bought(self, obj):
        # Return the books bought by the user
        return ', '.join([book.name for book in obj.books.all()])  # Assuming books are stored in a ManyToManyField named 'books'
    get_books_bought.short_description = 'Books Bought'  # Set a user-friendly name for the column
    
admin.site.register(User, UserAdmin)