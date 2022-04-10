import logging
from typing import Optional
from django.contrib.auth.models import User, Group
from django.core.handlers.wsgi import WSGIRequest

from django_auth_adfs.config import settings
from django_auth_adfs.backend import AdfsAuthCodeBackend

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist, PermissionDenied
import jwt

from . import provider
provider_config = provider.NautobotProviderConfig()

logger = logging.getLogger("django_auth_adfs")

class OAuth2(AdfsAuthCodeBackend):
    """
    Authentication backend to allow authenticating users against a
    Microsoft ADFS server with an authorization code.
    """
    def exchange_auth_code(self, authorization_code, request):
        logger.debug("Received authorization code: %s", authorization_code)
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.CLIENT_ID,
            'redirect_uri': provider_config.redirect_uri(request),
            'code': authorization_code,
        }
        if settings.CLIENT_SECRET:
            data['client_secret'] = settings.CLIENT_SECRET

        logger.debug("Getting access token at: %s", provider_config.token_endpoint)
        response = provider_config.session.post(provider_config.token_endpoint, data, timeout=settings.TIMEOUT)
        # 200 = valid token received
        # 400 = 'something' is wrong in our request
        if response.status_code == 400:
            if response.json().get("error_description", "").startswith("AADSTS50076"):
                raise MFARequired
            logger.error("ADFS server returned an error: %s", response.json()["error_description"])
            raise PermissionDenied

        if response.status_code != 200:
            logger.error("Unexpected ADFS response: %s", response.content.decode())
            raise PermissionDenied

        adfs_response = response.json()
        return adfs_response

    def validate_access_token(self, access_token):
        for idx, key in enumerate(provider_config.signing_keys):
            try:
                # Explicitly define the verification option.
                # The list below is the default the jwt module uses.
                # Explicit is better then implicit and it protects against
                # changes in the defaults the jwt module uses.
                options = {
                    'verify_signature': True,
                    'verify_exp': True,
                    'verify_nbf': True,
                    'verify_iat': True,
                    'verify_aud': True,
                    'verify_iss': True,
                    'require_exp': False,
                    'require_iat': False,
                    'require_nbf': False
                }
                # Validate token and return claims
                return jwt.decode(
                    access_token,
                    key=key,
                    algorithms=['RS256', 'RS384', 'RS512'],
                    audience=settings.AUDIENCE,
                    issuer=provider_config.issuer,
                    options=options,
                    leeway=settings.JWT_LEEWAY
                )
            except jwt.ExpiredSignatureError as error:
                logger.info("Signature has expired: %s", error)
                raise PermissionDenied
            except jwt.DecodeError as error:
                # If it's not the last certificate in the list, skip to the next one
                if idx < len(provider_config.signing_keys) - 1:
                    continue
                else:
                    logger.info('Error decoding signature: %s', error)
                    raise PermissionDenied
            except jwt.InvalidTokenError as error:
                logger.info(str(error))
                raise PermissionDenied

    def authenticate(self, request=None, authorization_code=None, **kwargs):
        # If loaded data is too old, reload it again
        provider_config.load_config()

        # If there's no token or code, we pass control to the next authentication backend
        if authorization_code is None or authorization_code == '':
            logger.debug("django_auth_adfs authentication backend was called but no authorization code was received")
            return

        adfs_response = self.exchange_auth_code(authorization_code, request)
        access_token = adfs_response["access_token"]
        user = self.process_access_token(access_token, adfs_response)
        user.token = access_token
        user.refresh_token = adfs_response["refresh_token"]
        return user

    def update_user_groups(self, user, claims=None):
        """
        Updates user group memberships based on the GROUPS_CLAIM setting.
        Args:
            user (django.contrib.auth.models.User): User model instance
            claims (dict): Claims from the access token
        """
        if django_settings.EXTERNAL_AUTH_DEFAULT_GROUPS:
            # Update the user's group memberships

            existing_groups = list(Group.objects.filter(name__in=django_settings.EXTERNAL_AUTH_DEFAULT_GROUPS).iterator())
            existing_group_names = frozenset(group.name for group in existing_groups)
            user.groups.set(existing_groups)
