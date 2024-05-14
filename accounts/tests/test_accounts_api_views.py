import pytest
from django.urls import reverse
from rest_framework import status
from django.test.client import Client


@pytest.fixture
def user_payload():
    params = {
        "first_name": "Teste",
        "last_name": "Teste",
        "email": "teste@gmail.com",
        "password": "Teste123@",
        "phone": "11999999999",
    }
    return params


@pytest.fixture
def user(django_user_model, user_payload):
    user = django_user_model.objects.create_user(**user_payload)
    user.is_active = True
    return user.save()


@pytest.fixture
def jwt_valid_token(client, user, user_payload):
    uri = reverse("rest_login")
    login_data = {"email": user_payload["email"], "password": user_payload["password"]}
    response = client.post(uri, login_data)
    return response.data["access"]


@pytest.mark.django_db
def test_register_api_view_return_status_code_201_CREATED(
    client: Client, user_payload: dict[str, str]
):
    uri = reverse("rest_user_register")
    response = client.post(uri, user_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers["content-type"] == "application/json"


@pytest.mark.django_db
def test_login_api_view_return_status_code_200_OK(user, client, user_payload):
    uri = reverse("rest_login")
    login_data = {"email": user_payload["email"], "password": user_payload["password"]}
    response = client.post(uri, login_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"


@pytest.mark.django_db
def test_me_api_view_return_status_code_200_OK(client, jwt_valid_token):
    uri = reverse("rest_user_me")
    response = client.get(uri, headers={"Authorization": f"Bearer {jwt_valid_token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
