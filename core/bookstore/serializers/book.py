from rest_framework import serializers
from bookstore.models import Book, BuyBook
from rest_framework import status
from bookstore.api.tools import CustomException



class BuyBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    def validate(self, attrs):
        if self.request and self.request.user.is_authenticated:
            user_cash = self.request.user.cash
            
            # Retrieve the book object
            try:
                book = Book.objects.get(id=attrs['book_id'])
            except Book.DoesNotExist:
                raise CustomException(
                    "Book not found",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
                
            buybook = BuyBook.objects.filter(user=self.request.user, book=book)
            if buybook.exists():
                raise CustomException(
                    "You have bought this book.",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if book.cost > user_cash:
                raise CustomException(
                    "please charge your account",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        else:
            raise serializers.ValidationError("Please authenticate first.")
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = self.request.user
        book_id = validated_data.get('book_id')
        book = Book.objects.get(id=book_id)
        
        # Subtract the book cost from the user's cash
        user.cash -= book.cost
        user.books.add(book)
        user.save()
        
        # Create the BuyBook object
        buy_book = BuyBook.objects.create(user=user, book=book)
        
        return book.link_download
    
class BookDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["link_download"]
        

class BookReturnSerializer(serializers.Serializer):

    def validate(self, attrs):
        # Check if the user is authenticated
        if not self.context['request'].user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated.")
        
        # Check if the user has bought the specified book
        user = self.context['request'].user
        book_id = self.context['book_id']
        if not BuyBook.objects.filter(user=user, book_id=book_id).exists():
            raise serializers.ValidationError("You have not purchased this book.")
        
        return attrs
    
class BookListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'link_download_10pages', 'get_categories', 'cost', 'pages_num', 'year']
        
        