from django.contrib import admin
from bookstore.models import BuyBook

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
    


admin.site.register(BuyBook, BuyBookAdmin)