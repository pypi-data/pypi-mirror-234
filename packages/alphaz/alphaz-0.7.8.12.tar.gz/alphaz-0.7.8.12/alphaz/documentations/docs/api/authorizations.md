
Route can be protected using the login system or admin rights.

# Login system

To protect a route using the login system you must specify: `logged=True`

```python
@route('protected', logged=True)
def protected_route():
    user = api.get_logged_user()
    return user
```

User information can be accessed using *get_logged_user* method.

# Admin

Admin could auto log to any user account on local mode

# Condition

To be an admin a user must have at least one condition:

- a **role** > 9
- specify the magic password has **admin** API parameter
- connect using an admin ip. The ips admin list must be defined in the **api.json** configuration files under the **key**=**admins_ips**

# How to use

If you met one of the admin condition you do not need any password in order to log has any of the user in the database.

You could be logged for specific routes using the **single route mode** or to any route using the **login/logout** system.


## Single route mode

- You could specifiy either admin_user_id={user_id} or admin_user_name={username} directly into any request in order to login with this user for this specific route.

!!! note "Exemple"
    /anyroute?admin_user_id=1000

## Login to the api

Use the route **/auth/su** in order to set an admin session that is valid until the end of the api runtime.

- You must specifiy either admin_user_id={user_id} or admin_user_name={username}

!!! note "Exemple"
    /auth/su?admin_user_id=1000

## Logout from the api

Use the route **/logout/su** in order to logout.