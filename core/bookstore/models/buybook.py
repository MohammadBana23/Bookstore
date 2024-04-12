from django.db import models
from bookstore.models import User, Book
from datetime import timedelta
from django.utils import timezone
from bookstore.api.tools import CustomException

def calculate_expiration_datetime():
    return timezone.now() + timedelta(minutes=60)

class BuyBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    expired_at = models.DateTimeField(default=calculate_expiration_datetime)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at', '-updated_at']
        
    # @staticmethod
    # def validate(user, book):
    #     query = BuyBook.objects.filter(
    #         user=user,
    #         book=book,
    #     )
    #     if query.exists():
    #         if timezone.now() >= query.first().expired_at:
    #             query.delete()
    #             raise CustomException(
    #                 "Your token expired",
    #                 "error",
    #                 status_code=status.HTTP_400_BAD_REQUEST
    #             )
    #         query.delete()
    #         return True
    #     else:
    #         VerificationToken.objects.filter(receiver=receiver).delete()
    #         raise CustomException(
    #                 "This token is not valid",
    #                 "error",
    #                 status_code=status.HTTP_400_BAD_REQUEST
    #             )