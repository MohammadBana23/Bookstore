from rest_framework import serializers
from ..api.tools import Email
from bookstore.models import VerificationToken

class RequestEmailTokenSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        # Check if the user is authenticated
        if self.request and self.request.user.is_authenticated:
            email = self.request.user.email
            token_object = VerificationToken.generate(receiver=email)
            sender = Email()
            sender.send_token_by_template(email, token_object.html, token_object.message)
            return "Token Sent"
        else:
            # Handle unauthenticated user case
            raise serializers.ValidationError("User is not authenticated")
