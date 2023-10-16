import secrets
import time
from flask import jsonify, request, abort
from pbu import list_to_json, Logger, default_options

login_cache = {}
api_key_cache = {}
# 1 week
SESSION_EXPIRATION_SECONDS = 60 * 60 * 24 * 7


def extract_token():
    """
    Extracts the Authorization header from the current request.
    :return: the extracted authorization token or None
    """
    key = "Authorization"
    if key in request.headers:
        return request.headers[key]

    if key in request.cookies:
        return request.cookies[key]

    return None


def generate_token():
    """
    Generates a new random hex token with length 16
    :return: a random string
    """
    return secrets.token_hex(16)


# authentication related classes and functions


class AuthenticationError(ConnectionRefusedError):
    """
    Error class used to handle authentication errors.
    """

    def __init__(self, message):
        """
        Create a new instance of an authentication error, whenever a request failed to authenticate
        :param message: an optional message to provide
        """
        super().__init__(message)


def perform_login_check(token):
    """
    Performs the actual login check on the token extracted from the header. It will check whether the token is
    registered with the backend and also if the session stored with the token is expired.
    :param token: the token provided by the user through the Authorization header of a HTTP request
    :return: the logged-in user object containing basic information about the user's identity
    :raise AuthenticationError in case the session is expired or the authorization token cannot be found in the current
    login state.
    """
    # regular HTTP authentication via React app / frontend
    if token in login_cache:
        login_data = login_cache[token]
        if time.time() - login_data["time"] > SESSION_EXPIRATION_SECONDS:
            # login session expired
            del login_cache[token]
            raise AuthenticationError("Login expired")
        else:
            # login session still active
            return login_data["user"]

    # if token not in the login state, return None
    raise AuthenticationError("Invalid authorization header")


def check_login_state(permission=None, allow_api_key=False):
    """
    Main function to be called from API endpoints to check if a user is logged in.
    This will extract the authorization token from the header, check it against the currently stored active sessions and
    handle any AuthenticationErrors that might occur by returning a 401 to the callee. If the request is authenticated,
    the associated user will be returned.
    :return: the authenticated user, if authentication was successful.
    :raise: AuthenticationError in case the login failed for whatever reason
    """
    try:
        token = extract_token()
        if token is not None and token.startswith("Token "):
            # API key auth
            if allow_api_key is False:
                logger = Logger("user_api")
                logger.error("API key access not allowed for the current endpoint.")
                abort(403)  # not enabled for this endpoint
            # check api key
            if token[6:] not in api_key_cache:
                raise AuthenticationError("Invalid authorization header")  # api key not registered
            user = api_key_cache[token[6:]]
        else:
            # fetch user the regular way
            user = perform_login_check(token)
        if permission is None or permission in user.permissions:
            return user
    except AuthenticationError as ae:
        logger = Logger("user_api")
        logger.exception(ae)
        abort(401)
        raise ae

    logger = Logger("user_api")
    logger.error("User {} doesn't have required privileges: {}".format(user.username, permission))
    abort(403)
    raise AuthenticationError("Insufficient privileges")


def fill_login_cache(user_store, token_store, use_api_keys):
    # clean up expired tokens
    token_store.clean_up_expired()
    # preload tokens into local cache
    existing_tokens = token_store.get_all()
    for token in existing_tokens:
        user = user_store.get(token.user_id)
        if user is not None:
            login_cache[token.token] = {
                "user": user,
                "time": time.time(),
            }

    # fill api key cache
    if use_api_keys is True:
        for user in user_store.get_users_with_api_key():
            api_key_cache[user.api_key] = user


def remove_from_login_cache(user_id):
    remove_token = []
    for token in login_cache:
        if login_cache[token]["user"].id == user_id:
            remove_token.append(token)
    for token in remove_token:
        del login_cache[token]


def update_login_cache(user):
    for token in login_cache:
        if login_cache[token]["user"].id == user.id:
            login_cache[token]["user"] = user
    for token in api_key_cache:
        if api_key_cache[token].id == user.id:
            api_key_cache[token] = user


_DEFAULT_OPTIONS = {
    "api_prefix": "/api/user",
    "token_expiration": 24 * 60 * 60,  # 24h
    "default_permissions": [],
    "user_admin_permission": "admin",
    "no_user_management": False,
    "api_keys": False,
    "allow_own_profile_edit": False,
    "page_size": 25,
}


def _remove_password(user_json):
    if "password" in user_json:
        del user_json["password"]
    return user_json


def register_endpoints(app, user_store, token_store, options_override={}):
    options = default_options(_DEFAULT_OPTIONS, options_override)

    api_prefix = options["api_prefix"]
    admin_permission = options["user_admin_permission"]
    default_perms = options["default_permissions"]
    skip_user_management = options["no_user_management"] is True
    use_api_keys = options["api_keys"] is True
    allow_own_profile_edit = options["allow_own_profile_edit"] is True
    page_size = options["page_size"]

    # load still active user tokens
    if token_store is not None:
        fill_login_cache(user_store, token_store, use_api_keys)

    @app.route("{}/login".format(api_prefix), methods=["POST"])
    def login_user():
        body = request.get_json()
        username, password = body["username"], body["password"]
        # run login
        user = user_store.login_with_password(username, password)
        if user is None:
            abort(401)

        # create and store token
        token = generate_token()
        if token_store is not None:
            token_store.create(user.id, token)
        login_cache[token] = {"user": user, "time": time.time()}
        # return logged in user
        resp = jsonify({"user": _remove_password(user.to_json()), "token": token})
        resp.set_cookie("Authorization", token, max_age=SESSION_EXPIRATION_SECONDS)
        return resp

    @app.route("{}/logout".format(api_prefix), methods=["DELETE"])
    def logout_user():
        check_login_state()
        auth_token = extract_token()
        if auth_token is not None and auth_token in login_cache:
            del login_cache[auth_token]
        return jsonify({"status": True})

    @app.route(api_prefix, methods=["GET"])
    def login_check():
        user = check_login_state()
        return jsonify(_remove_password(user.to_json()))

    @app.route("{}/users".format(api_prefix), methods=["GET"])
    def get_all_users():
        check_login_state(admin_permission)
        # extract page parameter
        page = request.args.get("page")
        if page is None:
            page = 0
        else:
            try:
                page = int(page)
            except ValueError:
                abort(400)

        users, total = user_store.get_all(page_size=page_size, page=page)
        return jsonify({
            "users": list(map(lambda x: _remove_password(x), list_to_json(users))),
            "total": total,
        })

    if use_api_keys:
        @app.route("{}/key".format(api_prefix), methods=["POST"])
        def create_api_token():
            user = check_login_state()
            # create new key
            new_key = user_store.create_api_key(user.id)
            # remove old key from cache
            if user.api_key is not None and user.api_key in api_key_cache:
                del api_key_cache[user.api_key]
            # add updated user to api cache and return new key
            user.api_key = new_key
            api_key_cache[new_key] = user
            return jsonify({"apiKey": new_key})

        @app.route("{}/key".format(api_prefix), methods=["DELETE"])
        def revoke_api_token():
            user = check_login_state()
            if user.api_key is not None and user.api_key in api_key_cache:
                del api_key_cache[user.api_key]
            user.api_key = None
            update_login_cache(user)
            user_store.revoke_api_key(user.id)
            return jsonify({"apiKey": None})

    if not skip_user_management:
        @app.route("{}/users/<user_id>/permissions".format(api_prefix), methods=["POST"])
        def update_user_permissions(user_id):
            check_login_state(admin_permission)
            body = request.get_json()
            permissions = body["permissions"]

            updated_user = user_store.update_permissions(user_id, permissions)
            update_login_cache(updated_user)
            return jsonify(_remove_password(updated_user.to_json()))

        @app.route("{}/users/<user_id>/profile".format(api_prefix), methods=["POST"])
        def update_user_profile(user_id):
            user = check_login_state()
            if admin_permission not in user.permissions:
                if allow_own_profile_edit is False:
                    abort(403)
                if allow_own_profile_edit is True and user_id != str(user.id):
                    abort(403)

            # all good, we have permission
            updated_user = user_store.update_profile(user_id, request.get_json())
            update_login_cache(updated_user)
            return jsonify(_remove_password(updated_user.to_json()))

        @app.route("{}/users/<user_id>".format(api_prefix), methods=["DELETE"])
        def delete_user(user_id):
            check_login_state(admin_permission)
            existing = user_store.get(user_id)
            if existing is None:
                abort(404)
            # delete user
            user_store.delete(user_id)
            # clean up session token
            remove_from_login_cache(user_id)
            # clean up api token
            if use_api_keys and existing.api_key is not None and existing.api_key in api_key_cache:
                del api_key_cache[existing.api_key]
            return jsonify({
                "userId": user_id,
                "deleted": True,
            })

        # create user
        @app.route("{}/users".format(api_prefix), methods=["POST"])
        def create_new_user():
            check_login_state(admin_permission)
            body = request.get_json()

            # extract permissions
            effective_perms = default_perms
            if "permissions" in body:
                effective_perms = body["permissions"]

            # handle local users
            if "username" not in body or body["username"] is None or body["username"].strip() == "":
                abort(400)
            if "password" not in body or body["password"] is None or body["password"].strip() == "":
                abort(400)
            existing = user_store.get_by_username(body["username"])
            if existing is not None:
                abort(400)
            new_user = user_store.create_local_user(body["username"], body["password"], effective_perms)
            return jsonify(_remove_password(new_user.to_json()))

    # change own password
    @app.route("{}/password".format(api_prefix), methods=["POST"])
    def change_own_password():
        user = check_login_state()
        body = request.get_json()
        if "newPassword" not in body or body["newPassword"] == "" or "oldPassword" not in body or \
                body["oldPassword"] == "":
            abort(400)

        # attempt to log in with old password
        old_user = user_store.login_with_password(user.username, body["oldPassword"])
        if old_user is None:
            abort(403)  # invalid old password

        user = user_store.change_password(user.id, body["newPassword"])
        return jsonify(_remove_password(user.to_json()))

    if not skip_user_management:
        # change another users password as admin
        @app.route("{}/users/<user_id>/password".format(api_prefix), methods=["POST"])
        def change_other_users_password(user_id):
            check_login_state(admin_permission)
            body = request.get_json()
            if "password" not in body or body["password"] is None:
                abort(400)
            existing = user_store.get(user_id)
            if existing is None:
                abort(404)

            updated = user_store.change_password(user_id, body["password"])
            return jsonify(_remove_password(updated.to_json()))
