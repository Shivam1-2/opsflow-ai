"""Production settings scaffold.

This is not a complete production deployment. It keeps DEBUG off,
requires a real secret, and keeps CORS closed unless explicitly configured.
"""

from .base import *  # noqa: F403
from .base import SECRET_KEY, env_list

DEBUG = False

if not SECRET_KEY or SECRET_KEY == "change-me":
    raise ValueError("DJANGO_SECRET_KEY must be set to a strong value in production.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ValueError("DJANGO_ALLOWED_HOSTS must be set in production.")

CORS_ALLOWED_ORIGINS = env_list("DJANGO_CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
