"""
A decorator adding basic API key authentication to a flask route

Example Usage:
>>> @app.route("/login", methods=["POST"])
... @require_api_key("Njk0MjAgeW91ciBzdHJpbmcgNjk0MjA")
... def login():
...     # route code here #
"""

import functools
import flask


def require_api_key(api_key: str):
    """A decorator adding basic API key authentication to a flask route\n
    Notes
    -----
    This requires the client request to contain the API key in a parameter called "key"\n
    Parameters
    ----------
    api_key : str
        The true API key required in order to successfully authenticate the user/client\n
    Example Usage
    -------------
    >>> @app.route("/login", methods=["POST"])
    ... @require_api_key("Njk0MjAgeW91ciBzdHJpbmcgNjk0MjA")
    ... def login():
    ...     # route code here #
    """

    def decorator_require(route_func):
        @functools.wraps(route_func)
        def wrapper_require(*args, **kwargs):
            if not flask.request.args.get("key"):
                flask.abort(401)  # Unauthorized: unknown user requires authentication
            if flask.request.args.get("key") == api_key:
                return route_func(*args, **kwargs)
            flask.abort(403)  # Forbidden: known client denied access to the content

        return wrapper_require

    return decorator_require
