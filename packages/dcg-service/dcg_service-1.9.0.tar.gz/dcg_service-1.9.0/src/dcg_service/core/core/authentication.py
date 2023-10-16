import jwt
from flask_babel import lazy_gettext as _
from .exceptions import AuthException
from .utils import get_user_obj


from settings import SIGNING_KEY, JWT_ALGORITHMS


def jwt_get_user_permissions_from_payload_handler(payload):
    """
    Override this function if permissions is formatted differently in payload
    """
    return payload.get('permissions')


def jwt_get_user_from_payload_handler(payload):
    """
    Override this function if permissions is formatted differently in payload
    """
    return payload.get('user', '') or None


def authenticate_credentials(payload):
    """
    Returns an active user that matches the payload's user id.
    """

    user = jwt_get_user_from_payload_handler(payload)
    # fetch the user data from the token.
    if not user:
        raise AuthException(_('Invalid Authorization header. No user found.'))

    permissions = jwt_get_user_permissions_from_payload_handler(payload)
    user = get_user_obj(user)

    user.permissions = permissions

    user.is_authenticated = True

    if user.user_type == 'ADMIN':
        user.is_superuser = True
    elif user.user_type == 'AGENT':
        user.is_agent = True

    return user


def get_authorization_header(header):
    """
    Return request's 'Authorization:' header.
    """
    auth = header.get('Authorization')
    return auth


def get_internal_key_header(header):
    """
    Return request's 'Internal-Service-Key:' header.
    """
    internal_key = header.get('Internal-Service-Key')
    return internal_key


def authenticate(token):
    """
    Returns a two-tuple of `User` and token if a valid signature has been
    supplied using JWT-based authentication.  Otherwise, returns `None`.
    """
    if not token:
        raise AuthException(
            _('Invalid Authorization header. No credentials provided.'))
    auth = token.split()
    auth_header_prefix = 'bearer'
    if auth[0].lower() != auth_header_prefix:
        raise AuthException(_('Invalid prefix.'))
    if len(auth) == 1:
        raise AuthException(
            _('Invalid Authorization header. No credentials provided.'))
    elif len(auth) > 2:
        raise AuthException(
            _('Invalid Authorization header or Credentials string or should not contain spaces.'))
    jwt_value = auth[1]
    try:
        payload = jwt.decode(jwt_value, SIGNING_KEY, algorithms=JWT_ALGORITHMS)
    except jwt.InvalidSignatureError:
        raise AuthException(_('Invalid signature.'))
    except jwt.ExpiredSignatureError:
        raise AuthException(_('Signature expired.'))
    except jwt.DecodeError:
        raise AuthException(_('Error decoding signature.'))
    except Exception:
        raise AuthException(_('Error decoding signature'))

    user = authenticate_credentials(payload)
    return user
