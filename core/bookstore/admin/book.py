from django.contrib import admin
from bookstore.models import Book, Category
from bookstore.api.tools import MinIO, save_ten_pages_pdf
from django.conf import settings
import io

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
        
        book_file = form.cleaned_data.get('book_file')
        file_name = book_file.name
        file_data = book_file.read()
        file_size = book_file.size
        
        # Convert file_data to a BytesIO object
        file_data_io = io.BytesIO(file_data)
        
        # Initialize MinIO client
        minio = MinIO(settings.MINIO_ACCESSKEY, settings.MINIO_SECRETKEY, settings.MINIO_ENDPOINT)
        
        # Upload full PDF to MinIO
        minio.upload_file("bookstore", file_name, file_data_io, file_size)
        
        # Get download link for full PDF
        download_link = minio.get_download_link("bookstore", file_name)
        if download_link:
            obj.link_download = download_link
        else:
            print("Failed to generate download link for full PDF.")
        
        # Generate 10 pages PDF and convert it to bytes
        ten_pages_pdf_bytes, ten_pages_pdf_name , ten_pages_pdf_size= save_ten_pages_pdf(file_data, file_name)
        
        
        # Upload 10 pages PDF to MinIO
        minio.upload_file("bookstore-10pages", ten_pages_pdf_name, ten_pages_pdf_bytes, ten_pages_pdf_size)
        
        # Get download link for 10 pages PDF
        download_link_10pages = minio.get_download_link("bookstore-10pages", ten_pages_pdf_name)
        if download_link_10pages:
            obj.link_download_10pages = download_link_10pages
        else:
            print("Failed to generate download link for 10 pages PDF.")
        
        # Save the Book object
        super().save_model(request, obj, form, change)
        # Save the Book object with the updated download links
        obj.save()
    
admin.site.register(Book, BookAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    
admin.site.register(Category, CategoryAdmin)
