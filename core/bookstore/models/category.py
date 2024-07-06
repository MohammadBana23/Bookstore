from django.db import models


class Category(models.Model):
    CATEGORY_NAME_CHOICES = [
        ("EDUCATIONAL", "علمی"),
        ("GENERAL", "عمومی"),
        ("HISTORICAL", "تاریخی"),
    ]
    name = models.CharField(max_length=20, choices=CATEGORY_NAME_CHOICES, blank=False, null=False)
    
    def __str__(self):
        return self.name