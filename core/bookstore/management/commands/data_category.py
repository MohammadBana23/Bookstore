from django.core.management.base import BaseCommand
from bookstore.models import Category
from faker import Faker


class Command(BaseCommand):
    help = 'Create a category fake data'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()
    
    def handle(self, *args, **options):
        Category.objects.create(
            name="مذهبی"
        )
        Category.objects.create(
            name="تاریخی"
        )
        Category.objects.create(
            name="علمی"
        )
        Category.objects.create(
            name="ترسناک"
        )
        Category.objects.create(
            name="روانشناسی"
        )
        self.stdout.write(self.style.SUCCESS('Successfully created categories.'))

        