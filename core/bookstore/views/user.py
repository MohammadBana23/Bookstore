from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import ChargeAccountSerializer
from rest_framework.permissions import IsAuthenticated
class ChargeAccountView(GenericAPIView):
    serializer_class = ChargeAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Ensure that the request object is passed to the serializer
        serializer = self.serializer_class(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)  # Ensure serializer is valid
        serializer.save()  # Update user's cash field
        return Response({"message": "Account charged successfully."}, status=status.HTTP_200_OK)
