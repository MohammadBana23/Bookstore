
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from bookstore.serializers import BuyBookSerializer, BookDownloadSerializer
from rest_framework import status
from ..models import Book, BuyBook
from bookstore.api.tools import CustomException
from rest_framework import serializers



class BuyBookCreateGenericAPIView(GenericAPIView):
    serializer_class = BuyBookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)  # Ensure serializer is valid
        data = {"download link":serializer.save()}
        return Response(data, status=status.HTTP_201_CREATED)
    
class BookDownloadAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDownloadSerializer

    def get_object(self):
        book = super().get_object()
        user = self.request.user
        
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Please authenticate first.")

        # Check if the user has purchased the book
        try:
            buy_book = BuyBook.objects.get(user=user, book=book)
        except BuyBook.DoesNotExist:
            raise CustomException(
                "You have not purchased this book.",
                "error",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return book
    