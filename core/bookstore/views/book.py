
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.mixins import RetrieveModelMixin
from bookstore.serializers import (BuyBookSerializer, BookDownloadSerializer, 
                                    BookListSerializer,BookReturnSerializer)
from rest_framework import status
from ..models import Book, BuyBook
from bookstore.api.tools import CustomException
from rest_framework import serializers



class BuyBookCreateGenericAPIView(generics.GenericAPIView):
    serializer_class = BuyBookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)  # Ensure serializer is valid
        data = {"download link":serializer.save()}
        return Response(data, status=status.HTTP_201_CREATED)
    
class BookDownloadAPIView(generics.RetrieveAPIView):
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
    
class BookReturnAPIView(generics.GenericAPIView):
    serializer_class = BookReturnSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request, 'book_id': self.kwargs['pk']})
        serializer.is_valid(raise_exception=True)

        # Get the user and book
        user = request.user
        book_id = self.kwargs['pk']
        book = Book.objects.get(pk=book_id)

        # Add the cost of the book to user's cash
        user.cash += book.cost
        user.books.remove(book)
        user.save()

        # Delete the BuyBook record
        BuyBook.objects.filter(user=user, book_id=book_id).delete()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
    
class BookListGenericAPIView(generics.ListAPIView):
    serializer_class = BookListSerializer
    queryset = Book.objects.all()