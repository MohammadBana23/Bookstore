from django.db import models
from bookstore.models.category import Category


class Book(models.Model):
    LANGUAGE_CHOICES = (
        ("ENGLISH", "English"),
        ("PERSIAN", "Persian"),
    )
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    picture = models.ImageField(upload_to="book-images/", null=True, blank=True)
    book_file = models.FileField(upload_to="books/", null=True, blank=True)
    link_download = models.CharField(max_length=1023, null=True, blank=True)
    link_download_10pages = models.CharField(max_length=1023, null=True, blank=True)
    cost = models.IntegerField(default=0)
    language = models.CharField(max_length=255, choices=LANGUAGE_CHOICES, default="ENGLISH")
    year = models.IntegerField(null=True, blank=True)
    pages_num = models.IntegerField(null=True, blank=True, default=0)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_categories(self):
        return "\n".join([c.name for c in self.categories.all()])
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at', '-updated_at']