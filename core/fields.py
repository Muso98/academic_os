from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class EncryptedField(models.TextField):
    description = "Field that encrypts data with Fernet"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            return value
        f = Fernet(settings.ENCRYPTION_KEY)
        # Ensure value is string
        return f.encrypt(str(value).encode()).decode()

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        f = Fernet(settings.ENCRYPTION_KEY)
        try:
            return f.decrypt(value.encode()).decode()
        except Exception as e:
            # If decryption fails (maybe changed key or garbage data), return raw or None
            # For now, return raw to avoid data loss, but log it in real app
            return value

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return str(value)
