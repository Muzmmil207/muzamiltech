from .base import *

if not DEBUG:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    DATABASES = {
        "default": dj_database_url.config(
            default="postgres://muzamil:tS3wrVF7crOQtzfbIOsqnmhXyENqkFTa@dpg-chkehn64dadfmsk7eheg-a.oregon-postgres.render.com/config_mg71_pybs",
            conn_max_age=60,
        )
    }

    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
        
    ADMINS = [
        ("Muzamil Ali", "muzmmila141@gmail.com"),
    ]
    # Email setting
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'mly88207@gmail.com'
    EMAIL_HOST_PASSWORD = 'mwnieujlittzbzlz'
    RECIPIENT_ADDRESS = 'muzmmila141@gmail.com'
    EMAIL_USE_TLS = True
    SERVER_EMAIL = 'mly88207@gmail.com'