from django.urls import path
from bookstore.views import (
    SignUpView, LoginView, RequestTokenView, ChargeAccountView,
    BuyBookCreateGenericAPIView, BookDownloadAPIView
)

urlpatterns = [
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
    path("request/token/", RequestTokenView.as_view(), name='request-token'),
    path("charge-account/", ChargeAccountView.as_view(), name='charge-account'),
    path("buy-book/", BuyBookCreateGenericAPIView.as_view(), name='buy-book'),
    path("book/<int:pk>/download/", BookDownloadAPIView.as_view(), name='book-retrieve'),
]