# Flask Authentication

Flask Endpoints for User Management and Authentication Middleware

1. [Endpoints](#endpoints)
2. [Authentication](#authentication)

## Endpoints

```python
from frappyflaskauth import register_endpoints
from flask import Flask

app = Flask(__name__)
# create store instances for users
user_store = ...
# this is a minimal configuration
register_endpoints(app, user_store)
```

**Parameters**

- `app` - the Flask app instance
- `user_store` - an store class providing user related methods
- `token_store` - optional - if you want login sessions to survive a server restart
- `options_override` - default `{}` - a dictionary containing configuration options that override the defaults:

**Options**

- `api_prefix` - default `/api/user` - the API prefix used for all endpoints (e.g. `/api/user/login`)
- `token_expiration` - default `86400` - the number of seconds a login session is valid for before it expires
- `default_permissions` - default `[]` - the initial permissions any user receives on creation (local users)
- `user_admin_permission` - default `admin` - the permission a user requires to be able to invoke user management 
 endpoints like update permissions, delete users, fetch all users, update passwords of other users.
- `no_user_management` - default `False` - if you don't want any user management endpoints to be registered
- `api_keys` - default `False` - if you need API keys to access endpoints (integrated into `check_login_state`). API
 keys are provided in the `Authorization` header prefixed with `Token $KEY` (where `$KEY` is the user's API key)
- `allow_own_profile_edit` - default `False` - if this is set to true, any user can update *their own* profile info
 (`user.profile`).
- `page_size` - default `25` - the number of users returned with the `/users` endpoint (lists all users)

## Authentication

To check if a user is authenticated and get the currently logged in user in your own endpoints, simply use the 
`check_login_state` function. It will 

- extract the authentication header
    - return a 401, if no authentication header is present
- check if that header is valid and associated with a user
    - return a 401, if the header is invalid or expired
- has the option to check if the associated user has a specific permission
    - return a 403, if the user doesn't have the required permission
- return the user object to the caller, if all checks are successful
- specific restrictions for API key access
    - return a 403, if the user tries to use an API key to access an endpoint not configured for this

```python
from frappyflaskauth import check_login_state
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/my-endpoint", methods=["GET"])
def my_custom_endpoint():
    user = check_login_state("view")
    # execution will only go past this point, if user is logged in AND has "view" permission
    print(user.id, user.permissions)  # this is the currently logged in user
    return jsonify({})

@app.route("/api/my-endpoint", methods=["GET"])
def my_logged_in_endpoint():
    _ = check_login_state()  # simply check if the user is logged in, ignore the returned user
    return jsonify({})

@app.route("/api/my-endpoint", methods=["GET"])
def my_api_key_enabled_endpoint():
    _ = check_login_state(allow_api_key=True)
```

Parameters:

- `permission`, default `None` which is a string that is checked against the `user.permissions` field (which is a `list`)
- `allow_api_key`, default `False` which is a flag enabling API keys to access the endpoint protected by this function
 call.
