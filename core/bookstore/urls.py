from django.urls import path
from bookstore.views import (
    SignUpView, LoginView, GetTestBookGenericAPIView
)

urlpatterns = [
    path('signup/' , SignUpView.as_view(), name='signup'),
    path('login/' , LoginView.as_view(), name='login'),
    path('test-book', GetTestBookGenericAPIView.as_view(), name='test-book'),
]