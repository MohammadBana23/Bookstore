from django.urls import path
from bookstore.views import (
    SignUpView, LoginView, RequestTokenView, ChargeAccountView,
    BuyBookCreateGenericAPIView, BookDownloadAPIView, BookReturnAPIView
)

urlpatterns = [
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
    path("request/token/", RequestTokenView.as_view(), name='request-token'),
    path("charge-account/", ChargeAccountView.as_view(), name='charge-account'),
    path("book/buy/", BuyBookCreateGenericAPIView.as_view(), name='book-buy'),
    path("book/<int:pk>/download/", BookDownloadAPIView.as_view(), name='book-download'),
    path("book/<int:pk>/return/", BookReturnAPIView.as_view(), name='book-return'),
]