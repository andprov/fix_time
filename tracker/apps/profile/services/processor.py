from typing import Union

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from apps.profile.models import User


class AccountActivator:
    @staticmethod
    def _get_user(uidb64: str) -> Union[User, None]:
        try:
            return User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    @staticmethod
    def _activate_account(user: Union[User, None]) -> None:
        user.is_active = True
        user.save()

    def execute(self, uidb64: str, token: str) -> bool:
        user: Union[User, None] = self._get_user(uidb64)
        if user and default_token_generator.check_token(user, token):
            self._activate_account(user)
            return True
        return False
