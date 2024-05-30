from django.contrib.auth import _get_user_session_key, _get_backends, user_logged_in
from django.middleware.csrf import rotate_token
from django.utils.crypto import constant_time_compare

SESSION_KEY = "_auth_user_id"
BACKEND_SESSION_KEY = "_auth_user_backend"
HASH_SESSION_KEY = "_auth_user_hash"
REDIRECT_FIELD_NAME = "next"


def login(request, user, backend=None):
    print('this is login function')

    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ""
    if user is None:
        user = request.user
    if hasattr(user, "get_session_auth_hash"):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash
                and not constant_time_compare(
            request.session.get(HASH_SESSION_KEY, ""), session_auth_hash
        )
        ):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                "You have multiple authentication backends configured and "
                "therefore must provide the `backend` argument or set the "
                "`backend` attribute on the user."
            )
    else:
        if not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash

    print(request.session[SESSION_KEY])
    print(request.session[BACKEND_SESSION_KEY])
    print(request.session[HASH_SESSION_KEY])

    if hasattr(request, "user"):
        print('inja ejra shod')
        request.user = user
        print(user)
        print(request.user)
        print(user.__class__)
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)


def get_user_by_type(user):
    user_model_type = user._meta.model_name
    if user_model_type == 'student' or user_model_type == 'staff' or user_model_type == 'teacher':
        return_user = user.user
    else:
        return_user = user
    return return_user
