from django.contrib.auth.backends import ModelBackend
from .models import User
import logging


class EmailBackend(ModelBackend):
    def authenticate(self, request, username =None, password=None, **kwargs):
        logger = logging.getLogger(__name__)
        logger.debug(f"Attempting authentication for email: {username}")
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
