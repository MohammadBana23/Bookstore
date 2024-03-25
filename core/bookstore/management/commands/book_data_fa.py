from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from bookstore.models import Book
from random import choice

class Command(BaseCommand):
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        
        success_count = 0
        failed_count = 0
        try:
            Book.objects.create(
                name = "Django for Beginners",
                category = "EDUCATIONAL",
                link_download = "https://bookstoreminio.darkube.app/python-test-bucket/Django%20for%20Beginners.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=KWY4DX9UZJPKWHARHS66%2F20240325%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240325T082526Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJLV1k0RFg5VVpKUEtXSEFSSFM2NiIsImV4cCI6MTcxMTM5NjgwNywicGFyZW50IjoiYTRsMHRna3doWmJDM002cjFMSmtickRIYzlQUVFpeTkifQ.zGWeDg9D8YLknuQvtVAuXQIlNmt6DnDxKGkTfk4tSQ1tQ32JAZ2rBozf5Rxx4MdRbJwJ4WCCeWQqoMdSpUOlDg&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=9612f1cef106bcf1650fe77132154004ee3d23f11095982d96c2ae43af303a15",
                cost = 500,
                language = "ENGLISH",
                year = 2018,
                pages_num = 224,
                is_special = True,
                created_at = timezone.now(),
                updated_at = timezone.now(),
            )
            Book.objects.create(
                name = "Agile Software Engineering",
                category = "GENERAL",
                link_download = "https://bookstoreminio.darkube.app/python-test-bucket/Agile%20Software%20Engineering.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=KWY4DX9UZJPKWHARHS66%2F20240325%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240325T082038Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJLV1k0RFg5VVpKUEtXSEFSSFM2NiIsImV4cCI6MTcxMTM5NjgwNywicGFyZW50IjoiYTRsMHRna3doWmJDM002cjFMSmtickRIYzlQUVFpeTkifQ.zGWeDg9D8YLknuQvtVAuXQIlNmt6DnDxKGkTfk4tSQ1tQ32JAZ2rBozf5Rxx4MdRbJwJ4WCCeWQqoMdSpUOlDg&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=6da60d9513fcfbb72a469035eeb8df80d1dad50003880bf8e941d938f572a792",
                cost = 300,
                language = "PERSIAN",
                year = 2021,
                pages_num = 25,
                created_at = timezone.now(),
                updated_at = timezone.now(),
            )
            Book.objects.create(
                name = "Django for Professionals",
                category = "EDUCATIONAL",
                link_download = "https://bookstoreminio.darkube.app/python-test-bucket/Django%20for%20Professionals.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=KWY4DX9UZJPKWHARHS66%2F20240325%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240325T092405Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJLV1k0RFg5VVpKUEtXSEFSSFM2NiIsImV4cCI6MTcxMTM5NjgwNywicGFyZW50IjoiYTRsMHRna3doWmJDM002cjFMSmtickRIYzlQUVFpeTkifQ.zGWeDg9D8YLknuQvtVAuXQIlNmt6DnDxKGkTfk4tSQ1tQ32JAZ2rBozf5Rxx4MdRbJwJ4WCCeWQqoMdSpUOlDg&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=c1739c86b8628f1a7646506f53916259af43f11257985245f625962605f9c128",
                cost = 600,
                language = "ENGLISH",
                year = 2019,
                pages_num = 373,
                is_special = True,
                created_at = timezone.now(),
                updated_at = timezone.now(),
            )
            
            success_count += 1
        except Exception as e:
            print(e)
            failed_count += 1
        self.stdout.write(self.style.SUCCESS("=================================================="))
        self.stdout.write(self.style.SUCCESS("Book Faker Tasks Completed!"))
        self.stdout.write(self.style.SUCCESS(f"Total Records: {failed_count+success_count}"))
        self.stdout.write(self.style.ERROR(f"Failed Records: {failed_count}"))
        self.stdout.write(self.style.WARNING(f"Success Records: {success_count}"))