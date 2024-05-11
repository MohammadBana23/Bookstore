from django.urls import path
from bookstore.views import (
    SignUpView, LoginView, RequestTokenView, ChargeAccountView,
    BuyBookCreateGenericAPIView, BookDownloadAPIView, BookReturnAPIView,
    BookListGenericAPIView
)
app_name = 'api-v1'
urlpatterns = [
    
    # registration url pattern
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
    
    #generate token url pattern
    path("request/token/", RequestTokenView.as_view(), name='request-token'),
    
    # charge the user account url pattern
    path("charge-account/", ChargeAccountView.as_view(), name='charge-account'),
    
    # books url pattern
    path("books/", BookListGenericAPIView.as_view(), name='book-list'),
    path("book/buy/", BuyBookCreateGenericAPIView.as_view(), name='book-buy'),
    path("book/<int:pk>/download/", BookDownloadAPIView.as_view(), name='book-download'),
    path("book/<int:pk>/return/", BookReturnAPIView.as_view(), name='book-return'),
]