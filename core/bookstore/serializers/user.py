from rest_framework import serializers
from bookstore.models import User, VerificationToken
from bookstore.api.tools.api import CustomException
from rest_framework import status

class ChargeAccountSerializer(serializers.Serializer):
    cash = serializers.IntegerField(required=True)
    token = serializers.IntegerField(required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # Check if the user is authenticated
        if self.request and self.request.user.is_authenticated:
            email = self.request.user.email
            
            # Validate the token
            try:
                VerificationToken.validate(email, attrs['token'])
            except CustomException as e:
                raise serializers.ValidationError(e.detail)
            
            # Validate the cash amount (positive integer)
            if attrs['cash'] <= 0:
                raise serializers.ValidationError("Cash amount must be a positive integer.")
            
            return attrs
        else:
            raise serializers.ValidationError("Please authenticate first.")
    
    def create(self, validated_data):
        # Retrieve the user instance
        user = self.request.user
        
        # Update the user's cash field
        user.cash += validated_data['cash']
        user.save()
        
        return user
