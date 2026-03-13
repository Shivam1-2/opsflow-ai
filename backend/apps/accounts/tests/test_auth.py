import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_valid_credentials_authenticate(api_client, user_factory):
    user_factory(email="operator@example.com", password="correct-password")
    response = api_client.post(
        reverse("auth-login"),
        {"email": "operator@example.com", "password": "correct-password"},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["email"] == "operator@example.com"
    assert "password" not in response.json()


@pytest.mark.django_db
def test_invalid_credentials_fail(api_client, user_factory):
    user_factory(email="operator@example.com", password="correct-password")
    response = api_client.post(
        reverse("auth-login"),
        {"email": "operator@example.com", "password": "wrong-password"},
        format="json",
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.django_db
def test_inactive_user_cannot_authenticate(api_client, user_factory):
    user_factory(email="inactive@example.com", password="correct-password", is_active=False)
    response = api_client.post(
        reverse("auth-login"),
        {"email": "inactive@example.com", "password": "correct-password"},
        format="json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_unauthenticated_me_fails(api_client):
    response = api_client.get(reverse("auth-me"))
    assert response.status_code in {401, 403}


@pytest.mark.django_db
def test_authenticated_me_succeeds(authenticated_client):
    response = authenticated_client.get(reverse("auth-me"))
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == authenticated_client.user.email
    assert "password" not in body
    assert "organization" in body
