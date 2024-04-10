from django.contrib import admin
from bookstore.models import VerificationToken


class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "receiver" , "created_at", "updated_at", "expired_at"]
    readonly_fields = ("created_at", "updated_at", "expired_at")
    search_fields = [
        "receiver",
    ]
    ordering = ["id", "created_at", "updated_at"]
    list_filter = ["created_at", "expired_at"]

admin.site.register(VerificationToken, VerificationTokenAdmin)