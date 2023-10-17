from django.urls import path, include
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from urllib.parse import urljoin
import requests
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest

import logging
logger = logging.getLogger(__name__)
User = get_user_model()


def include_auth_urls():
    return include([path(r"login/", login), path(r"logout/", logout)])


def include_internal_urls():
    return include([path(r"sessions/flush/", flush_session_view),])


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    auth_redirect_url: str = request.build_absolute_uri().split("?")[0]
    # since the app is running in container, it might mistakenly
    # assume it's not using SSL/TLS
    auth_redirect_url = auth_redirect_url.replace("http:", "https:")
    auth_code: str = request.query_params.get("code", "")
    app_redirect_url: str = request.query_params.get("state", "")

    client_id = settings.IDENTITY_CLIENT_ID
    client_secret = settings.IDENTITY_CLIENT_SECRET

    token_url = urljoin(settings.IDENTITY_HOST, "/o/token/")
    reply = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": auth_redirect_url,
        },
        auth=(client_id, client_secret),
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            auth_redirect_url,
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    tokens = reply.json()
    introspect_url = urljoin(settings.IDENTITY_HOST, "/o/introspect/")
    introspect_response = requests.post(
        introspect_url,
        data={"token": tokens["access_token"],},
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            tokens["access_token"],
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    email = introspect_response.json()["username"]
    # here we can also get additional user info, GUID, etc
    user, _ = User.objects.get_or_create(
        email__iexact=email, defaults={"username": email, "email": email}
    )
    request.session["email"] = email

    return HttpResponseRedirect(redirect_to=app_redirect_url)


def _get_public_identity_host(request):
    """
    Doing it in a super dumb way for now, lets see if we need smth more complex later
    :return:
    """
    host = request.get_host()
    domain_name = host.split("//")[-1]
    parent_domain = ".".join(domain_name.split(".")[1:])
    return "https://id." + parent_domain


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def logout(request):
    request.session.flush()
    state: str = request.query_params.get("state", "")
    redirect_url = urljoin(_get_public_identity_host(request), "auth/logout/")
    response = HttpResponseRedirect(redirect_to=f"{redirect_url}?state={state}")
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def flush_session_view(request):
    """
    this is supposed to be served under a protected router only accessible from inside the network
    :param request:
    :return:
    """
    email = request.data["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseBadRequest({"reason": "no such user!"})
    delete_all_unexpired_sessions_for_user(user)
    return Response({"flushed_session": f"{email}"})


def delete_all_unexpired_sessions_for_user(user):
    """
    This is pretty inefficient, and will log the user out across all devices
    however, on our scale should work fine.
    We can upgrade this setup later to store session/user pairs in a separate
    custom table
    :param user:
    :return:
    """
    logger.info(f"clearing sessions for user {user.email}, {user.id}")
    all_sessions = Session.objects.filter(expire_date__gte=now())

    user_sessions = [
        session.pk
        for session in all_sessions
        if user.email == session.get_decoded().get("email")
    ]
    logger.debug(f"found {len(user_sessions)} user sessions")
    count, sessions_deleted = Session.objects.filter(pk__in=user_sessions).delete()
    logger.debug(count)
    logger.debug(sessions_deleted)
