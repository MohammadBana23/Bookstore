import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from bookstore.models.user import User

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username = 'test-user-by-email',
        email = 'testing@gmail.com',
        password ='#test-pass12345#'
    )
    return user


@pytest.mark.django_db
class TestLogin:
    url = reverse('api-v1:login')

    def test_login_not_registered_email_response_404(self, api_client , common_user):
        # user is not registered and wont be found (404)
        response = api_client.post(self.url, data={
                "email": "testing_@gmail.com",
                "password": "#failed-pass12345#"
            })
        assert response.status_code == 404

    def test_login_correct_email_response_200(self, api_client , common_user):
        response = api_client.post(self.url, data={
                "email": 'testing@gmail.com',
                "password": "#test-pass12345#"
            })
        assert response.status_code == 200