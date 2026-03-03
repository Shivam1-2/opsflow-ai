import logging

import redis
from django.conf import settings
from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=HTTP_200_OK)


class ReadyView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        dependencies = {
            "database": _check_database(),
            "redis": _check_redis(),
        }
        healthy = all(status == "ok" for status in dependencies.values())
        payload = {
            "status": "ok" if healthy else "unavailable",
            "dependencies": dependencies,
        }
        if not healthy:
            logger.warning("Readiness check failed: %s", dependencies)
            return Response(payload, status=HTTP_503_SERVICE_UNAVAILABLE)
        return Response(payload, status=HTTP_200_OK)


def _check_database() -> str:
    try:
        connection.ensure_connection()
        return "ok"
    except Exception:
        logger.exception("PostgreSQL readiness check failed")
        return "unavailable"


def _check_redis() -> str:
    try:
        client = redis.from_url(settings.REDIS_URL)
        client.ping()
        return "ok"
    except Exception:
        logger.exception("Redis readiness check failed")
        return "unavailable"
