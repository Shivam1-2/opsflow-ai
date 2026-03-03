from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_endpoint_returns_ok():
    client = APIClient()
    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_ready_endpoint_returns_healthy_dependencies(monkeypatch):
    redis_client = MagicMock()
    redis_client.ping.return_value = True
    monkeypatch.setattr("apps.core.views.redis.from_url", lambda _url: redis_client)

    client = APIClient()
    response = client.get(reverse("health-ready"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "dependencies": {
            "database": "ok",
            "redis": "ok",
        },
    }
