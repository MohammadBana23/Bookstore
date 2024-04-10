from django.core.validators import validate_email as validateEmail
from rest_framework import serializers


class EmailValidationMixin:
    
    def validate_email(self, email):
        try:
            validateEmail(email)
            return email
        except Exception:
            raise serializers.ValidationError(
                    "This email address is not valid",
                    "invalid email"
                )