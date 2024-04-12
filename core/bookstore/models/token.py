import random
import string
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from ..api.tools import CustomException
from rest_framework import status

def calculate_expiration_datetime():
    return timezone.now() + timedelta(minutes=30)

def create_random_token():
    return ''.join(random.choice(string.digits) for x in range(6))

class VerificationToken(models.Model):

    # --------------------------------- Model Fields ------------------------- #
    receiver = models.CharField(
        'Receiver',
        max_length=64, unique=True
    )
    token = models.CharField('Token', max_length=6, default=create_random_token)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    expired_at = models.DateTimeField(default=calculate_expiration_datetime)

    @property
    def html(self):
        return render_to_string(
                f'token.html', {"token" : self.token, "receiver" : self.receiver}
            )
    
    @property
    def message(self):
        return render_to_string(
            f'token.txt' , {"token" : self.token, "receiver" : self.receiver}
        )
    
    @staticmethod
    def generate(receiver):

        time_limit_second = 120
        
        query = VerificationToken.objects.filter(receiver=receiver)
        if query.exists():
            if timezone.now() <= query.first().updated_at + timedelta(seconds=time_limit_second):
                return query.first()
            else:
                query = VerificationToken.objects.get(receiver=receiver)
                query.token = create_random_token()
                query.save()
                return query
        
        token = VerificationToken(
            receiver=receiver,
        )
        token.save()
        return token

    @staticmethod
    def validate(receiver, token):
        query = VerificationToken.objects.filter(
            receiver=receiver,
            token=token,
        )
        if query.exists():
            if timezone.now() >= query.first().expired_at:
                query.delete()
                raise CustomException(
                    "Your token expired",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            query.delete()
            return True
        else:
            VerificationToken.objects.filter(receiver=receiver).delete()
            raise CustomException(
                    "This token is not valid",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
    def __str__(self):
        return str(self.id)