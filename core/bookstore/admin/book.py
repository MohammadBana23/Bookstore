from django.contrib import admin
from bookstore.models import Book, Category


class BookAdmin(admin.ModelAdmin):
    model = Book
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
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
