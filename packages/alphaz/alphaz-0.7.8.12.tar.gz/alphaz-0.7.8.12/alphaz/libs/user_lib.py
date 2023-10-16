# CORE
from sqlalchemy import or_
from core import core

DB = core.db

# MODULES
import datetime
from sqlalchemy.orm import sessionmaker

# MODELS
from ..models.user import AlphaUser
from ..models.database import main_definitions as defs
from ..models.database.users_definitions import User

# LIBS
from . import secure_lib, string_lib, api_lib


def __get_user_data_by_identifier_and_password(
    identifier,
    password_attempt,
    no_password_check: bool = False,
) -> AlphaUser | None:
    user = __get_user_data(identifier, ["username", "mail"])

    if user is not None and password_attempt is not None:
        if no_password_check:
            return user
        valid_password = secure_lib.compare_passwords(password_attempt, user.password)
        if valid_password:
            return user
    return None


def get_user_data_from_login(
    login, password=None, no_password_check: bool = False
) -> AlphaUser | None:
    """Get user data from database either by mail or username.

    Args:
        login ([type]): [description]
        password ([type]): [description]

    Returns:
        [type]: [description]
    """
    user = __get_user_data_by_identifier_and_password(
        login, password, no_password_check=no_password_check
    )
    return user


def get_user_data_from_database(
    value,
    columns: str | list[str],
    activity: bool = False,
    force_local: bool = False,
    scoped_session: bool = False,
) -> dict | None:
    """Get the user associated with given column."""
    user = None
    if type(columns) == str:
        columns = [columns]
    filters = [or_(*[User.__dict__[column] == value for column in columns])]

    if DB.user_api is None or force_local:
        if not scoped_session:
            user = DB.select(
                User,
                filters=filters,
                first=True,
                relationship=True,
                # disabled_relationships=["notifications"],
            )
            if user is not None and activity:
                with user.query.session.begin(subtransactions=True):
                    user.last_activity = datetime.datetime.now()
                    if user.mail is None:
                        user.mail = "-"
            user = user.to_json() if user is not None else None
        else:
            user_engine = DB.get_engine(bind="USERS")
            Session = sessionmaker(bind=user_engine)
            scoped_session = Session()

            try:
                # Commencer une transaction avec la session spécifique
                with scoped_session.begin():
                    # Mettre à jour la personne avec la session spécifique
                    user = (
                        scoped_session.query(User)
                        .filter(*filters)
                        .first()
                    )

                    if user is not None and activity:
                        # Stocker la valeur de user.mail dans une variable
                        user_mail = "-" if user.mail is None else user.mail

                        scoped_session.query(User).filter(
                            *filters
                        ).update(
                            {
                                User.last_activity: datetime.datetime.now(),
                                User.mail: user_mail,
                            }
                        )
                        scoped_session.commit()
                        user = {
                            column.key: getattr(user, column.key)
                            for column in user.__table__.columns
                        }
            except Exception as e:
                # Si une erreur se produit, annuler tous les changements avec la session spécifique
                scoped_session.rollback()
                raise e

            finally:
                # Fermer la session spécifique
                scoped_session.close()
    else:
        user_api = DB.user_api + "/user/data"
        user = api_lib.get_api_data(
            user_api,
            params={"value": value, "columns": columns, "activity": activity},
        )
    return user if user is not None else None


def __get_user_data(
    value, columns: str | list[str], activity: bool = False
) -> AlphaUser | None:
    user = get_user_data_from_database(value, columns, activity=activity)
    alpha_user = AlphaUser.map_from_dict(user) if user is not None else None
    return alpha_user


def get_user_data_by_id(user_id, activity: bool = False) -> AlphaUser | None:
    if not string_lib.is_number(user_id):
        return None
    return __get_user_data(user_id, "id", activity=activity)


def get_user_data_by_logged_token(token) -> AlphaUser | None:
    return __get_user_data(token, "token")


def get_user_data_by_registration_token(token) -> AlphaUser | None:
    return __get_user_data(token, "registration_token")


def get_user_data_by_password_reset_token(token) -> AlphaUser | None:
    return __get_user_data(token, "password_reset_token")


def get_user_data_by_mail(mail) -> AlphaUser | None:
    return __get_user_data(mail, "mail")


def get_user_data_by_username(username, activity: bool = False) -> AlphaUser | None:
    return __get_user_data(username, "username", activity=activity)


def get_user_data_by_telegram_id(telegram_id) -> AlphaUser | None:
    return __get_user_data(telegram_id, "telegram_id")


def update_users():
    """Update all users."""
    # Set expired states if needed
    query = "UPDATE user SET role = 0 WHERE expire <= UTC_TIMESTAMP();"
    DB.execute_query(query, None)

    # Set expired states if needed
    query = "UPDATE user SET password_reset_token = 'consumed' WHERE password_reset_token_expire <= UTC_TIMESTAMP();"
    DB.execute_query(query, None)

    # Remove non activated in time accounts
    query = "DELETE FROM user WHERE role = -1 AND date_registred + INTERVAL 15 MINUTE > UTC_TIMESTAMP();"
    DB.execute_query(query, None)

    # Remove expired sessions
    query = "DELETE FROM user_session WHERE expire <= UTC_TIMESTAMP();"
    DB.execute_query(query, None)


def is_valid_mail(email):  # TODO: update
    return (
        DB.select(
            defs.MailingList,
            filters=[defs.MailingList.email == email],
            distinct=defs.MailingList.email,
            unique=defs.MailingList.email,
            first=True,
        )
        != None
    )


def get_all_address_mails():
    return DB.select(
        defs.MailingList, distinct=defs.MailingList.email, unique=defs.MailingList.email
    )