from re import search
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from bookstore.models import User
from bookstore.api.tools.api import CustomException

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' , 'password2']

    def validate(self, attrs):
        # check if password2 is the same as password
        if attrs["password2"] != attrs["password"]:
            raise CustomException(
                "رمزعبور ها یکسان نیستند!",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # validate password
        try:
            validate_password(attrs["password"])
        except:
            raise CustomException(
                "رمزعبور وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # password2 is no longer needed
        attrs.pop("password2")
        
        result = validate_email(attrs["email"])
        if result == "E":
            """email is given"""
            q = User.objects.filter(email=attrs["email"])
            if q.exists():
                raise CustomException(
                    "کاربری با این ایمیل وجود دارد.",
                    "error",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        elif result == "Error":
            """not email is detected"""
            raise CustomException(
                "ایمیل وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            phone="09111111111",    
            password=validated_data["password"],
        )

        # get access and refresh
        data = generate_JWT_access_refresh_token(user)
        return data


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # username can be phone or email
        # check is the phone_or_email is valid
        print("$$$$$$$$$$$$$$$$$$$$", attrs)
        email = attrs["email"]
        result = validate_email(email)

        if result == "Error":
            raise CustomException(
                "ایمیل وارد شده صحیح نمیباشد.",
                "error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CustomException(
                "کاربری با این اطلاعات وجود ندارد.",
                "error",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except:
            raise CustomException(
                "مشکلی در احراز هویت کاربر بوجود آمده است.",
                "error",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # authenticating user
        # authenticate function will return None
        # if user.is_active equals to false
        user = authenticate(email=attrs["email"], password=attrs["password"])

        # is user password be incorrect, raise an exception
        try:
            refresh = self.get_token(user)
        except:
            raise CustomException(
                "رمزعبور به درستی وارد نشده است.",
                "error",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        update_last_login(None, user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return data
    
"""Functions"""
def generate_JWT_access_refresh_token(user):
    """
    this function will generate a JWT access refresh token
    for the given user
    """
    refresh = RefreshToken.for_user(user)
    data = {"refresh": str(refresh), "access": str(refresh.access_token)}
    return data

def validate_email(value):
    if search(r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", value):
        return "E"
    else:
        return "Error"