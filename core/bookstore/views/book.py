
from rest_framework.response import Response
from rest_framework import generics
from bookstore.serializers import (BuyBookSerializer, BookDownloadSerializer, 
                                    BookListSerializer,BookReturnSerializer)
from rest_framework import status
from ..models import Book, BuyBook
from bookstore.api.tools import CustomException
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated



class BuyBookCreateGenericAPIView(generics.GenericAPIView):
    serializer_class = BuyBookSerializer
    
    # POST method to create a BuyBook record
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)  # Ensure serializer is valid
        data = {"download link":serializer.save()}
        return Response(data, status=status.HTTP_201_CREATED)
    
class BookDownloadAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDownloadSerializer
    
    # Retrieve a specific book for download
    def get_object(self):
        book = super().get_object()
        user = self.request.user
        
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Please authenticate first.")

        # Check if the user has purchased the book
        try:
            BuyBook.objects.get(user=user, book=book)
        except BuyBook.DoesNotExist:
            raise CustomException(
                "You have not purchased this book.",
                "error",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return book
    
class BookReturnAPIView(generics.GenericAPIView):
    serializer_class = BookReturnSerializer

    # POST method to return a book that current user bought it
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
    
class BookListGenericAPIView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]
        
    # GET method to list books based on user permissions
    def get(self, request):
        if request.user.is_special:
            self.queryset = Book.objects.all()
        else:
            self.queryset = Book.objects.filter(is_special=False)
        serializers = self.serializer_class(self.queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)