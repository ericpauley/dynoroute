from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from allauth.account.auth_backends import AuthenticationBackend
from allauth.account.app_settings import AuthenticationMethod
from allauth.account import app_settings
User = get_user_model()

class CaseInsensitiveModelBackend(AuthenticationBackend):
    """
    By default ModelBackend does case _sensitive_ username authentication, which isn't what is
    generally expected.  This backend supports case insensitive username authentication.
    """
    def _authenticate_by_username(self, **credentials):
        username_field = app_settings.USER_MODEL_USERNAME_FIELD
        if not username_field or not 'username' in credentials:
            return None
        try:
            # Username query is case insensitive
            query = {username_field+'__iexact': credentials["username"], "gym":credentials.get("gym")}
            user = User.objects.get(**query)
            if user.check_password(credentials["password"]):
                return user
        except User.DoesNotExist:
            return None

    def _authenticate_by_email(self, **credentials):
        # Even though allauth will pass along `email`, other apps may
        # not respect this setting. For example, when using
        # django-tastypie basic authentication, the login is always
        # passed as `username`.  So let's place nice with other apps
        # and use username as fallback
        email = credentials.get('email', credentials.get('username'))
        if email:
            users = User.objects.filter(Q(email__iexact=email)
                                        | Q(emailaddress__email__iexact=email), gym=credentials.get("gym"))
            for user in users:
                if user.check_password(credentials["password"]):
                    return user
        return None
