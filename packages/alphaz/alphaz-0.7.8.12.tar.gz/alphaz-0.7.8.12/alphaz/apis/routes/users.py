# CORE
from core import core

API = core.api

# UTILS
from ...utils.api import ADMIN_USER_ID_PUBLIC, ADMIN_USER_NAME_PUBLIC, route, Parameter

# MODELS
from ...models.main import AlphaException

# LIBS
from ...libs import user_lib, secure_lib

from ..users import users


@route("user/infos", logged=True)
def user_infos():
    return API.get_logged_user()


@route(
    "/user/data",
    parameters=[
        Parameter("value", required=True),
        Parameter("columns", ptype=list[str], required=True),
        Parameter("activity", ptype=bool),
    ],
)
def user_data():
    return user_lib.get_user_data_from_database(**API.gets(), force_local=True)


@route(
    "/register",
    methods=["POST"],
    parameters=[
        Parameter("mail", required=True),
        Parameter("username", required=True),
        Parameter("password", required=True),
        Parameter("password_confirmation", required=True),
    ],
)
def register():
    if API.get_logged_user() is not None:
        raise AlphaException("logged")
    return users.try_register_user(**API.gets())


@route("/password", parameters=[Parameter("password")], admin=True)
def password():
    return secure_lib.secure_password(**API.gets())


@route(
    "/register/validation",
    methods=["POST"],
    parameters=[Parameter("tmp_token", required=True)],
)
def register_validation():
    if API.get_logged_user() is not None:
        raise AlphaException("logged")
    users.confirm_user_registration(**API.gets())


@route(
    "/auth",
    methods=["POST"],
    parameters=[
        Parameter("username", required=True),
        Parameter("password", required=True),
    ],
)
def login():
    return users.try_login(**API.gets())


@route(
    "/auth/su",
    methods=["POST"],
    parameters=[ADMIN_USER_ID_PUBLIC, ADMIN_USER_NAME_PUBLIC],
    admin=True,
)
def su_login():
    return users.try_su_login(**API.gets())


@route(
    "/ldap/users",
    parameters=[
        Parameter("filters", required=True, ptype=str),
    ],
)
def get_ldap_users():
    from ..users import users, ldap  # TODO: modify

    return ldap.get_ldap_users(**API.gets())


@route(
    "/password/lost",
    methods=["POST"],
    parameters=[
        Parameter("username", required=False),
        Parameter("mail", required=False),
    ],
)
def password_lost():
    if API.get_logged_user() is not None:
        raise AlphaException("logged")
    if API["username"] is None and API.get["mail"] is None:
        raise AlphaException("inputs")
    users.ask_password_reset(
        API["username"] if API.get["mail"] is None else API.get["mail"]
    )


@route(
    "/password/reset",
    methods=["GET", "POST"],
    parameters=[
        Parameter("tmp_token", required=True),
        Parameter("password", required=True),
        Parameter("password_confirmation", required=True),
    ],
)
def password_reset_validation():
    if API.get_logged_user() is not None:
        raise AlphaException("logged")
    users.confirm_user_password_reset(**API.gets())


@route("/logout", cache=False, logged=False, methods=["GET", "POST"])
def logout():
    users.logout()


@route("/logout/su", cache=False, logged=False, methods=["GET", "POST"])
def logout_su():
    users.logout_su()


@route(
    "/profile/password",
    logged=True,
    methods=["POST"],
    parameters=[
        Parameter("password", required=True),
        Parameter("password_confirmation", required=True),
    ],
)
def reset_user_password():
    users.try_reset_password(**API.gets())
