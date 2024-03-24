from django.db import models


class Book(models.Model):
    CATEGORY_CHOICES = (
        ("GENERAL", "general"),
        ("EDUCATIONAL", "educational"),
        ("HISTORICAL", "historical"),
        ("CHILDISH", "childish"),
    )
    LANGUAGE_CHOICES = (
        ("ENGLISH", "English"),
        ("PERSIAN", "Persian"),
    )
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="GENERAL")
    picture = models.ImageField(null=True, blank=True)
    file = models.CharField(max_length=5111)
    cost = models.IntegerField(default=0)
    language = models.CharField(max_length=255, choices=LANGUAGE_CHOICES, default="ENGLISH")
    year = models.IntegerField(null=True, blank=True)
    pages_num = models.IntegerField(null=True, blank=True, default=0)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at', '-updated_at']