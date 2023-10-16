
The api is automatically configured from the `api.jon` file. See [Configuration](configuration.md) for further details on how to use it.

### Main

- workers: In order to specify the numbers of workers

```json
"workers": 6
```

- routes_no_log: In order to specify the routes where log must be ignored

```json
"routes_no_log": ["//status", "//static", "//dashboard"],
```

- models: In order to specify the **Flask-SqlAlchemy** models definitions paths

```json
"models": ["models.database"]
```

- routes: In order to specify the routes definitions paths

```json
"routes": ["apis.routes"]
```

- ssl: In order to activate ssl mode

```json
"ssl": false
```

- threaded: In order to activate the threaded mode

```json
"threaded": false
```

- config: In order to activate pass configuration to Flask **api** class

```json
"config": {
    "MYSQL_DATABASE_CHARSET": "utf8mb4",
    "SQLALCHEMY_TRACK_MODIFICATIONS": false,
    "SQLALCHEMY_POOL_RECYCLE": 299,
    "SQLALCHEMY_POOL_TIMEOUT": 30,
    "SQLALCHEMY_POOL_SIZE": 10,
    "JWT_SECRET_KEY": "a_secret_key",
    "JSON_SORT_KEYS": false
}
```

### Mails

In order to specify the mails configurations

```json
"mails": {
    "mail_server": {
        "host": "",
        "mail": "",
        "password": "",
        "port": 465,
        "server": "",
        "ssl": true,
        "tls": false
    }
}
```

### Auth

In order to specify the auth mode

```json
"auth": {
    "mode": "ldap",
    "ldap": {
        "server": "ldap://path_to_ldap",
        "baseDN": "ou=people,dc=a_name,dc=com",
        "users_filters": "(|(uid={uid})(mail={mail})(cn={cn}))",
        "user_filters": "(|(uid={username})(mail={username})(cn={username}))",
        "user_data": {
            "givenName": "name",
            "sn": "lastname",
            "c": "area",
            "st-locationdescription": "location",
            "st-seatnumber": "seat",
            "telephoneNumber": "phone-number"
        }
    },
    "users": {
        "a_user_name": {
            "user_permissions": ["SUPER_USER"]
        }
    }
},
```

### Reloader type

In order to specify the [Werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/) reloader type

```json
"reloader_type": "stat"
```

### Admin

In order to specify the admins configurations

```json
"admins": {"ips":["127.0.0.1"], "password":"a_password"},
```


### Dashboard

In order to configure the [Flask-Monitoring Dashboard](https://flask-monitoringdashboard.readthedocs.io/)

```json
"dashboard": {
    "dashboard": {
        "APP_VERSION": 1.0,
        "SAMPLING_PERIOD": 20,
        "ENABLE_LOGGING": true,
        "active": false
    },
    "authentication": {
        "USERNAME": "username",
        "PASSWORD": "",
        "GUEST_USERNAME": "guest",
        "GUEST_PASSWORD": ["guest1", "guest2"],
        "SECURITY_TOKEN": "a_security_token"
    },
    "database": {
        "DATABASE": "sqlite:///{{root}}/dashboard.db"
    }
}
```