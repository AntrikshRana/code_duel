from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
        if not username or not password:
            return None
        try:
            # Case-insensitive lookup for username or email
            user = User.objects.filter(username__iexact=username).first()
            if not user:
                user = User.objects.filter(email__iexact=username).first()
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None
        return None
