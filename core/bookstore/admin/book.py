from django.contrib import admin
from bookstore.models import Book, Category
from minio import Minio
from bookstore.api.tools import MinIO, save_ten_pages_pdf
from django.conf import settings
import os


class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = (
        "id",
        "name",
        "author",
        "publisher",
        "get_categories",
        "cost",
        "book_file",
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
    
    def save_model(self, request, obj, form, change):
        
        # Save the Book object
        super().save_model(request, obj, form, change)
        obj_file_path = obj.book_file.path
        obj_file_name = (obj_file_path.split("/")[-1]).split(".")[0]
        
        
        # Upload full PDF to MinIO
        minio = MinIO(settings.MINIO_ACCESSKEY, settings.MINIO_SECRETKEY, settings.MINIO_ENDPOINT)
        minio.upload_file(obj_file_path, "bookstore", obj_file_path.split("/")[-1])
        
        # Get download link for full PDF
        download_link = minio.get_download_link("bookstore", obj_file_path.split("/")[-1])
        if download_link:
            obj.link_download = download_link
            obj.save()
        else:
            print("Failed to generate download link for full PDF.")

        # Upload 10 pages PDF to MinIO
        url_path = save_ten_pages_pdf(obj.book_file.path)
        minio.upload_file(url_path, "bookstore-10pages", f'{obj_file_name}-10pages.pdf')
        
        # Get download link for 10 pages PDF
        download_link_10pages = minio.get_download_link("bookstore-10pages", f'{obj_file_name}-10pages.pdf')
        if download_link_10pages:
            obj.link_download_10pages = download_link_10pages
            obj.save()
        else:
            print("Failed to generate download link for 10 pages PDF.")

        # Remove the PDF file from the media directory
        try:
            os.remove(obj.book_file.path)
            os.remove(url_path)
            obj.book_file = None
            obj.save()
        except OSError:
            pass  # File doesn't exist or couldn't be deleted, ignore
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
