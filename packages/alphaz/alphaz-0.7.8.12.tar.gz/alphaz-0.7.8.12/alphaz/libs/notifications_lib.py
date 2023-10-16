from ..models.database.users_definitions import Notification, User

from core import core

db = core.db


def add_notifications(
    user, element_type, element_action, id, users=None, all_users=True
):
    return
    if all_users:
        users = db.select(
            User, distinct=User.id, columns=[User.id], filters=[User.id != user.id]
        )

    notifications = [
        Notification(
            user=x[0],
            user_from=user.id,
            element_type=element_type,
            element_action=element_action,
            element_id=id,
        )
        for x in users
    ]
    db.add(notifications)
