from urllib.parse import urljoin
from rest_framework import authentication
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import exceptions
import logging
import requests


User = get_user_model()
logger = logging.getLogger(__name__)


class IdentityAuthentication(authentication.BaseAuthentication):
    """
    This should be the first authentication that user goess through, since we always trust the local sessions
    So that we dont have to spam api requests to id service
    """

    def authenticate(self, request):
        email = request.session.get("email")
        if not email or (settings.IDENTITY_WHITELIST != 'all' and email not in settings.IDENTITY_WHITELIST):
            return None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")
        request.session["email"] = user.email
        return (user, None)


class IdentitySSOAuthentication(authentication.BaseAuthentication):
    """
    This should be the second authentication that a request goess through:
    When the user doesnt have the local session, we can see if the user has an active session with the id service
    and create local session based on that
    """

    def authenticate(self, request):
        shared_cookie = request.COOKIES.get("sso_shared_session")
        if not shared_cookie:
            # auth not attempted
            return None

        validate_url = urljoin(settings.IDENTITY_HOST, "internal/sessions/validate/")
        user_info_reply = requests.post(
            validate_url, json={"sso_session_cookie": shared_cookie},
        )

        try:
            user_info_reply.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = (
                "User info request failed",
                e.response.status_code,
                e.response.content,
            )
            logger.warning(message)
            return None

        user_info = user_info_reply.json()
        email = user_info["user"]["email"]
        user, _ = User.objects.get_or_create(
            email__iexact=email, defaults={"username": email, "email": email}
        )
        request.session["email"] = user.email
        return (user, None)


class IdentityAPIKeyAuthentication(authentication.BaseAuthentication):
    """
    This authentication is used when a user API key is sent
    When the client doesnt have the local session, we try to authenticate it on the ID service
    and create local session based on that
    """

    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_USER_API_KEY")
        if not api_key:
            # auth not attempted
            return None

        validate_url = urljoin(settings.IDENTITY_HOST, "internal/api_keys/validate/")
        user_info_reply = requests.post(validate_url, json={"api_key": api_key},)

        try:
            user_info_reply.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = (
                "User info request failed",
                e.response.status_code,
                e.response.content,
            )
            raise exceptions.AuthenticationFailed(message)
        user_info = user_info_reply.json()
        email = user_info["user"]["email"]
        user, _ = User.objects.get_or_create(
            email__iexact=email, defaults={"username": email, "email": email}
        )
        request.session["email"] = user.email
        return (user, None)
