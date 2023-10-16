# MODULES
import datetime, jwt, itertools, socket
import enum
from flask import request

# CORE
from core import core, API, DB

# MODELS
from ...models.user import AlphaUser, AlphaUserSession
from ...models.database.users_definitions import User, UserSession
from ...models.main import AlphaException, EnumStr
from ...models.api import AlphaRequest

# LIBS
from ...libs import user_lib, secure_lib, json_lib, mail_lib


class LoginModes(EnumStr):
    LDAP = enum.auto()
    NO_CONFIRMATION = enum.auto()


LOG = core.get_logger("users")
LOGIN_MODE = core.api.conf.get("auth/mode")
LOGIN_MODE = None if LOGIN_MODE is None else LOGIN_MODE.upper()

DATA_TO_JWT = {
    "id": "id",
    "username": "sub",
    "time": "iat",
    "permissions": "permissions",
}


# Serve for registration
def try_register_user(
    mail, username, password, password_confirmation, validation=True, infos=""
):
    userByMail = user_lib.get_user_data_by_mail(mail)
    userByUsername = user_lib.get_user_data_by_username(username)
    validation = False if LOGIN_MODE == LoginModes.NO_CONFIRMATION.value else validation

    if validation and (userByMail is not None) or (userByUsername is not None):
        if (
            userByMail.role is not None and userByMail.role < 0
        ) or userByUsername.role < 0:
            raise AlphaException("account_not_validated")
        raise AlphaException("account_duplicated")

    if password != password_confirmation:
        raise AlphaException("password_missmatch")

    '''mail_valid = validate_email(mail)
    if not mail_valid:
        return "mail_format"'''

    '''if not password_check_format(password):
        return "password_format"'''

    password_hashed = secure_lib.secure_password(password)

    # ADD CHECKS FOR LENGHT OF USERNAME/MAIL!!

    # Generate token
    token = secure_lib.get_token()

    parameters = {"token": token, "name": username, "mail": mail}

    if validation and not mail_lib.send_mail(
        mail_config="registration", parameters_list=[parameters]
    ):
        raise AlphaException("sending")

    DB.add(
        User(
            username=username,
            mail=mail,
            password=password_hashed,
            role=-1 if validation else 1,
            date_registred=datetime.datetime.now(),
            last_activity=datetime.datetime.now(),
            registration_token=token,
            infos=json_lib.jsonify_data(infos, string_output=True),
        )
    )
    return {"validation": validation}


def update_infos(user, infos) -> bool:
    if type(infos) != str:
        infos = json_lib.jsonify_data(infos, string_output=True)

    infos_user = (
        json_lib.jsonify_data(user.infos) if type(user.infos) != str else user.infos
    )
    if infos == infos_user:
        return True
    user_id = user.id
    if user.mail is not None:
        return DB.update(User, values={"infos": infos}, filters=[User.id == user_id])
    return None


def ask_password_reset(username_or_mail):
    user_by_mail = user_lib.get_user_data_by_mail(username_or_mail)
    user_by_username = user_lib.get_user_data_by_username(username_or_mail)

    user = user_by_mail if user_by_mail is not None else user_by_username

    # Generate token
    token = secure_lib.get_token()

    query = "UPDATE user SET password_reset_token = %s, password_reset_token_expire = UTC_TIMESTAMP() + INTERVAL 20 MINUTE WHERE id = %s;"
    values = (
        token,
        user.id,
    )

    if not DB.execute_query(query, values):
        raise AlphaException("sql_error")

    # MAIL
    parameters = {}
    parameters["mail"] = user.mail
    parameters["token"] = token
    parameters["username"] = user.username
    parameters["name"] = user.username

    mail_sent = mail_lib.send_mail(
        mail_config="password_reset", parameters_list=[parameters]
    )


def confirm_user_registration(tmp_token):
    if "consumed" in tmp_token:
        raise AlphaException("invalid_token")
    user = user_lib.get_user_data_by_registration_token(tmp_token)

    if user is None:
        raise AlphaException("not_found")

    # Set Role to 0 and revoke token
    user = DB.select(User, filters={"id": user.id}, first=True, json=False)
    if user is None:
        raise AlphaException("error")
    user.role = 0
    user.registration_token = "consumed"
    DB.commit()

    valid = True
    if not valid:
        raise AlphaException("error")


def infos_dict_from_ldap(ldap_structure: dict, ldap_data: dict) -> dict:
    added_infos = {}
    if ldap_structure is not None:
        for ldap_name, name in ldap_structure.items():
            added_infos[name] = ldap_data[ldap_name] if ldap_name in ldap_data else ""
            if type(added_infos[name]) == list:
                added_infos[name] = " ".join(
                    [
                        x.decode("utf-8") if hasattr(x, "decode") else x
                        for x in added_infos[name]
                    ]
                )
    return added_infos


def get_expire_datetime() -> datetime:
    defaults_validity = {
        "days": 7,
        "seconds": 0,
        "microseconds": 0,
        "milliseconds": 0,
        "minutes": 0,
        "hours": 0,
        "weeks": 0,
    }
    validity_config = API.conf.get("token/login/validity")
    validity_config = {
        x: y
        if (validity_config is None or not x in validity_config)
        else validity_config[x]
        for x, y in defaults_validity.items()
    }
    return datetime.datetime.now() + datetime.timedelta(**validity_config)


def get_encoded_jwt_from_user_data(user) -> str:
    extra_tokens = API.conf.get(
        f"auth/users/{user.username}/user_permissions", default=[]
    )
    if type(extra_tokens) == list:
        user.permissions.extend(extra_tokens)
    user.permissions = list(set(user.permissions))

    # Generate token
    user.time = int(datetime.datetime.now().timestamp())
    user_data_to_encode = {y: getattr(user, x) for x, y in DATA_TO_JWT.items()}
    user_data_to_encode["exp"] = int(get_expire_datetime().timestamp())
    user_data_to_encode["app"] = API.conf.get("name")
    user_data_to_encode["env"] = core.configuration

    encoded_jwt = jwt.encode(
        user_data_to_encode,
        API.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )
    try:  # TODO: remove
        encoded_jwt = encoded_jwt.decode("ascii")
    except Exception as ex:
        pass
    return encoded_jwt


def try_login(username: str, password: str, su: bool = False) -> AlphaUser:
    username = username.strip() if username else username
    user = API.get_logged_user()

    # if logged_user is not None:
    # raise AlphaException("user_already_logged")
    if not su and (user is None or user.username != username):
        if LOGIN_MODE == LoginModes.LDAP.value:
            from .ldap import check_ldap_credentials, LDAP_DATA

            valid_ldap = check_ldap_credentials(username, password)
            if valid_ldap is None:
                raise AlphaException("Wrong user or password")

            added_infos = infos_dict_from_ldap(LDAP_DATA, valid_ldap)

            user = user_lib.get_user_data_from_login(
                username, password, no_password_check=True
            )
            if user is None:
                try_register_user(
                    mail=valid_ldap["mail"] if "mail" in valid_ldap else "-",
                    username=username,
                    password=password,
                    password_confirmation=password,
                    validation=False,
                    infos=added_infos,
                )
                user = user_lib.get_user_data_from_login(
                    username, password, no_password_check=True
                )
            else:
                update_infos(user, added_infos)
        else:
            user = user_lib.get_user_data_from_login(username, password)
            if user is None:
                raise AlphaException("wrong_user_or_password")

            if user.role is None or user.role < 0:
                raise AlphaException("account_not_validated_by_email")
            elif user.role is None or user.role == 0:
                raise AlphaException("account_not_validated_by_an_admin")
        if not "JWT_SECRET_KEY" in API.config:
            raise AlphaException("Missing <JWT_SECRET_KEY> api parameter")
    elif su and user is None:
        user = API.get_su_user(username, username)

    if user is None:
        raise AlphaException("incorrect_username_or_password")

    expire = get_expire_datetime()
    token = get_encoded_jwt_from_user_data(user)

    try:
        ip_address = request.remote_addr
    except:
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ip_address = "127.0.0.1"

    # Add new token session related to user
    if not DB.add_or_update(
        UserSession(
            user_id=user.id,
            token=token,
            ip=ip_address,
            expire=expire,
        )
    ):
        raise AlphaException("Cannot update user session")

    return {
        **{
            x: y
            for x, y in user.to_json().items()
            if not x in DATA_TO_JWT or x in ["username", "id"]
        },
        "token": token,
        "valid_until": expire,
    }


def try_su_login(
    admin_user_id: str | None = None, admin_user_name: str | None = None
) -> AlphaUser:
    user_data = try_login(
        admin_user_name if admin_user_name is not None else admin_user_id, None, su=True
    )
    API.admin_token = user_data["token"]
    return user_data


def confirm_user_password_reset(tmp_token, password, password_confirmation):
    if "consumed" in tmp_token:
        raise AlphaException("consumed_token")

    user = user_lib.get_user_data_by_password_reset_token(DB, tmp_token)
    if user is None:
        raise AlphaException("invalid_token")

    try_reset_password(user, password, password_confirmation)


def try_reset_password(password, password_confirmation):
    if password != password_confirmation:
        raise AlphaException("password_missmatch")
    user = API.get_logged_user()

    '''if not password_check_format(password):
        return "password_format"'''
    # Set New password and revoke token
    password_hashed = secure_lib.secure_password(password)

    # Reset password
    query = "UPDATE user SET password = %s, password_reset_token = 'consumed' WHERE id = %s;"
    values = (
        password_hashed,
        user.id,
    )
    valid = DB.execute_query(query, values)
    if not valid:
        raise AlphaException("reset_error")

    # Reset all sessions as password changed
    query = "DELETE FROM user_session WHERE user_id = %s;"
    values = (user.id,)
    valid = DB.execute_query(query, values)
    if not valid:
        raise AlphaException("clean_error")


def logout():
    token = AlphaRequest.get_token()
    if token is None:
        raise AlphaException("token_not_specified")
    if not DB.delete(UserSession, filters={"token": token}):
        raise AlphaException("fail")


def logout_su():
    API.admin_token = None


def get_user_session_from_id(id: int) -> AlphaUserSession:
    return DB.select(
        UserSession,
        filters=[UserSession.user_id == id],
        first=True,
        dataclass=AlphaUserSession,
    )


def try_subscribe_user(mail, nb_days, target_role):
    user = user_lib.get_user_data_by_mail(mail)
    expired_date = datetime.datetime.now() + datetime.timedelta(days=nb_days)
    if user is not None:
        # Reset password
        query = "UPDATE user SET role = %s, expire = %s WHERE id = %s;"
        values = (
            target_role,
            expired_date,
            user.id,
        )
        valid = DB.execute_query(query, values)
        if not valid:
            AlphaException("update_error")
    AlphaException("unknow_user")
