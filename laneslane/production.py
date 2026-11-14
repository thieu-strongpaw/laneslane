"""Production settings for Cloudflare Tunnel -> loopback Apache/mod_wsgi."""
import os
import shlex
from django.core.exceptions import ImproperlyConfigured
from .settings import *  # noqa: F403


# Apache and management commands share one root-controlled configuration file.
# Override the path for validation or alternate installations.
ENV_FILE = Path(os.environ.get("DJANGO_ENV_FILE", "/etc/laneslane/production.env"))
if ENV_FILE.exists():
    for number, line in enumerate(ENV_FILE.read_text().splitlines(), 1):
        tokens = shlex.split(line, comments=True)
        if not tokens:
            continue
        if len(tokens) != 1 or "=" not in tokens[0]:
            raise ImproperlyConfigured(f"Invalid environment entry at line {number} in {ENV_FILE}")
        key, value = tokens[0].split("=", 1)
        os.environ.setdefault(key, value)


def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"Set {name} in the server environment.")
    return value


DEBUG = False
SECRET_KEY = required("DJANGO_SECRET_KEY")
if len(SECRET_KEY) < 50 or SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured("Use a new random DJANGO_SECRET_KEY of at least 50 characters.")
ALLOWED_HOSTS = [host.strip() for host in required("DJANGO_ALLOWED_HOSTS").split(",") if host.strip()]
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Set explicit production hostnames in DJANGO_ALLOWED_HOSTS.")
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

# Apache overwrites this header on the dedicated loopback tunnel listener.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

DATA_DIR = Path(os.environ.get("DJANGO_DATA_DIR", "/var/lib/laneslane"))
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATA_DIR / "db.sqlite3", "OPTIONS": {"timeout": 20}}}
MEDIA_ROOT = DATA_DIR / "media"
STATIC_ROOT = Path(os.environ.get("DJANGO_STATIC_ROOT", "/srv/laneslane/staticfiles"))

# SMTP is optional for browsing/contact details; configure it for password resets.
MAILERS = {"default": {
    "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
    "HOST": os.environ.get("SMTP_HOST", "localhost"),
    "PORT": int(os.environ.get("SMTP_PORT", "587")),
    "USERNAME": os.environ.get("SMTP_USERNAME", ""),
    "PASSWORD": os.environ.get("SMTP_PASSWORD", ""),
    "USE_TLS": True,
}}
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
