from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
    """
    By default ModelBackend does case _sensitive_ username authentication, which isn't what is
    generally expected.  This backend supports case insensitive username authentication.
    """
    def authenticate(self, username=None, password=None, gym=None):
        try:
            user = get_user_model().objects.get(username__iexact=username, gym=gym)
            if user.check_password(password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            return None
