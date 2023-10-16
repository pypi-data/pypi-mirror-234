from alphaz.models.database.users_definitions import Permission, Role
from core import core


DB = core.db
LOG = core.get_logger("api")


def get_permissions(
    name: str,
    page_index: int,
    page_size: int,
    order_by: str,
    direction: str,
    columns: list[str] = None,
):
    permissions = DB.select(
        Permission,
        filters=[Permission.key.like(name)],
        page=page_index,
        per_page=page_size,
        order_by_direction=direction,
        order_by=order_by,
        columns=columns,
        disabled_relationships={Permission.roles: [Role.permissions, Role.application]},
    )
    return permissions


def get_permissions_names(name: str):
    return DB.select(
        Permission,
        optional_filters={Permission.key: {"like": name}},
        unique=Permission.key,
        distinct=Permission.key,
        order_by=Permission.key.asc(),
    )


def get_permission(name: str):
    permission = DB.select(
        Permission,
        filters=[Permission.key == name],
        first=True,
        disabled_relationships={Permission.roles: [Role.permissions, Role.application]},
    )
    return permission


def create_permission(permission: Permission):
    return DB.add(permission)


def edit_permission(permission: Permission):
    if permission is not None and permission.roles is not None:
        for role in permission.roles:
            if hasattr(role, "permissions"):
                del role.permissions
    return DB.update(permission)


def delete_permission(key: str):
    return DB.delete(Permission, filters=[Permission.key == key])
