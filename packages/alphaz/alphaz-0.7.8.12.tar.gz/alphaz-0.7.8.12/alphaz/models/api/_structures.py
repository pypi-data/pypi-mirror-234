# MODULES
import os, jwt, itertools, sys, importlib, warnings, traceback, time, socket

# WSGI
try:
    from gevent.pywsgi import WSGIServer
except:
    pass

# WERKZEUG
from werkzeug.debug import DebuggedApplication

# FLASK
from flask import Flask, jsonify, request, Response, make_response
from flask_mail import Mail

import flask_monitoringdashboard

with warnings.catch_warnings():
    from flask_marshmallow import Marshmallow

from flask_statistics import Statistics
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin

# CONFIGURATIONS
from ...config.main_configuration import CONFIGURATION

# LIBS
from ...libs import (
    io_lib,
    os_lib,
    config_lib,
    secure_lib,
)

# MODELS
from ...models.logger import AlphaLogger
from ...models.main import AlphaException
from ...models.config import AlphaConfig
from ...models.json import AlphaJSONEncoder
from ...models.api import AlphaRequest

# LOCAL
from . import _colorations
from ._reloaders import reloader_loops
from ._route import Route


class AlphaFlask(Flask):
    admin_token: str | None = None

    def __init__(
        self,
        *args,
        config_name=None,
        configuration=None,
        root=None,
        core=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__initiated: bool = False
        self.pid = None
        self.conf = None
        self._port = None

        self.db = None
        self.db_cnx = {}
        self.admin_db = None

        self.cache_dir = ""

        # need to put it here to avoid warnings

        self.ma = Marshmallow(self)

        self.routes_objects = {}

        self.log: AlphaLogger = core.get_logger(CONFIGURATION.API_LOGGER_NAME)
        self.log_requests: AlphaLogger = core.get_logger(CONFIGURATION.HTTP_LOGGER_NAME)

        core_api_config = core.config.get_config("api", None)
        if core_api_config is not None:
            self.conf = core_api_config
            self.configuration = core.configuration
        else:
            print("   ", config_name, configuration, root, core.configuration)
            self.set_config(config_name, configuration, root)

        confs = self.conf.get("config")
        if confs is not None:
            if configuration == "local":
                local_ban_keys = ["SQLALCHEMY_POOL_TIMEOUT", "SQLALCHEMY_POOL_SIZE"]
                for local_ban_key in local_ban_keys:
                    if local_ban_key in confs:
                        del confs[local_ban_key]
            for key, value in confs.items():
                self.config[key] = value

    @property
    def port(self):
        if self._port is None:
            self._port = self.conf.get("port")
        return self._port

    @port.setter
    def port(self, value):
        self._port = int(value) if not isinstance(value, int) else value

    def set_config(self, name, configuration=None, root=None):
        self.log.info(
            f"Set <{configuration}> configuration for API from {name} in {root}"
        )
        self.config_path = root + os.sep + name + ".json"
        self.configuration = configuration

        self.conf = AlphaConfig(
            name=name,
            configuration=configuration,
            root=root,
            log=self.log,
            required=["directories/cache"],
        )  # root=os.path.dirname(os.path.realpath(__file__))

        if self.conf.get("routes_no_log"):
            _colorations.WerkzeugColorFilter.routes_exceptions = self.conf.get(
                "routes_no_log"
            )

    def set_error(
        self,
        status: str | AlphaException = "error",
        description: str | None = None,
        warning: int = 0,
    ):
        self.get_current_route().set_error(
            status=status, description=description, warning=warning
        )

    def set_status(self, status="success", description=None):
        self.get_current_route().set_status(status=status, description=description)

    def get_status(self) -> tuple[str, str]:
        return self.get_current_route().get_status()

    def set_warning(
        self,
        status: str | AlphaException = "warning",
        description: str | None = None,
    ):
        self.set_error(status=status, description=description, warning=1)

    def get_parameters(
        self,
        not_none: bool = False,
        without: list[str] = None,
        added: dict[str, object] = None,
        with_user_id: bool = False,
        with_user_permissions: bool = False,
        with_user: bool = False,
    ) -> dict[str, object]:
        """Get non private route parameters values as a dict.

        Returns:
            dict[str, object]: [description]
        """
        route = self.get_current_route()
        parameters = route.parameters
        parameters_values = {
            x: y.value
            for x, y in parameters.items()
            if not y.private and (not not_none or y.value is not None)
        }
        if without is not None:
            parameters_values = {
                x: y for x, y in parameters_values.items() if not x in without
            }
        if added is not None:
            for key, value in added.items():
                parameters_values[key] = value

        if any([with_user_id, with_user, with_user_permissions]):
            user = self.get_logged_user()
        if with_user_id:
            parameters_values["user_id"] = user.id if user is not None else None
        if with_user:
            parameters_values["user"] = user
        if with_user_permissions:
            parameters_values["user_permissions"] = (
                user.permissions if user is not None else None
            )
        return parameters_values

    def gets(
        self,
        not_none: bool = False,
        without: list[str] = None,
        added: dict[str, object] = None,
        with_user_id: bool = False,
        with_user_permissions: bool = False,
        with_user: bool = False,
    ) -> dict[str, object]:
        return self.get_parameters(**{x: y for x, y in locals().items() if x != "self"})

    def is_error(self) -> bool:
        return self.get_current_route().is_error()

    def is_warning(self) -> bool:
        return self.get_current_route().is_warning()

    def set_data(self, data):
        self.get_current_route().set_data(data)

    def set_file(self, directory, filename):
        self.get_current_route().set_file(directory, filename)

    def get_file(self, directory, filename, as_attachment=True):
        self.get_current_route().get_file(directory, filename, as_attachment)

    def set_html(self, page, parameters={}):
        self.get_current_route().set_html(page, parameters)

    def set_databases(self, db_cnx):
        self.db_cnx = {x.upper(): y for x, y in db_cnx.items()}
        if not CONFIGURATION.MAIN_DATABASE_NAME in self.db_cnx:
            self.log.error("You must define a <main> database")
            exit()

        uri = self.db_cnx[CONFIGURATION.MAIN_DATABASE_NAME]["cnx"]
        if ":///" in uri:
            io_lib.ensure_file(uri.split(":///")[1].split("?")[0])
        # db_type = self.db_cnx[CONFIGURATION.MAIN_DATABASE_NAME]["type"]
        self.config["SQLALCHEMY_DATABASE_URI"] = uri

        self.config["SQLALCHEMY_BINDS"] = {x: y["cnx"] for x, y in self.db_cnx.items()}

        # self.api.config["MYSQL_DATABASE_CHARSET"]           = "utf8mb4"
        # self.api.config["QLALCHEMY_TRACK_MODIFICATIONS"]    = True
        # self.api.config["EXPLAIN_TEMPLATE_LOADING"]         = True
        self.config["UPLOAD_FOLDER"] = self.root_path
        # self.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = False

    def run(self, *args, **kwargs):
        self.init_run()
        super().run(*args, **kwargs)

    def init(self, encode_rules={}):
        """routes = self.conf.get("routes")
        if routes is not None:
            for route in routes:
                try:
                    print(f"Import route {route}")
                    module = importlib.import_module(route)
                except Exception as ex:
                    self.log.critical(f"Cannot import routes from {route}", ex=ex)"""
        self.cache_dir = self.conf.get("directories/cache")

        """if routes is not None:
            self.log.info(f"Init api with routes: {', '.join(routes)}")"""

        # Flask configuration
        # todo: check JWT_SECRET_KEY: mandatory

        self.json_encoder = AlphaJSONEncoder
        for key_rule, fct in encode_rules.items():
            AlphaJSONEncoder.rules[key_rule] = fct

        self.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'

        # MAILS
        mail_config = self.get_config("mails/mail_server")

        if mail_config is not None:
            self.config.update(
                MAIL_USE_TLS=mail_config["tls"],
                MAIL_USE_SSL=mail_config["ssl"],
                MAIL_SERVER=mail_config["server"],
                MAIL_PORT=mail_config["port"],
                MAIL_USERNAME=mail_config["mail"],
                MAIL_PASSWORD=mail_config["password"],
            )
            self.mail = Mail(self)
        else:
            self.log.error(
                'Mail configuration is not defined ("mails/mail_server" parameter)'
            )

        if self.conf.get("toolbar"):
            self.log.info("Loaded debug toolbar")
            toolbar = DebugToolbarExtension(self)

        if self.conf.get("dashboard/dashboard/active"):
            self.log.info("Loaded dashboard")
            filepath = config_lib.write_flask_dashboard_configuration()
            if filepath is not None:
                self.log.info("Dashboard configured from %s" % filepath)
                flask_monitoringdashboard.config.init_from(file=filepath)
                flask_monitoringdashboard.bind(self)

        if self.conf.get("admin_databases"):
            self.log.info("Loaded admin databases interface")
            self.init_admin_view()

        # Base.prepare(self.db.engine, reflect=True)

    def init_admin_view(self):
        from ...libs import flask_lib  # TODO: change

        views = flask_lib.load_views(self.log)
        endpoints = [x.endpoint for x in views]

        from ..database.views import views as alpha_views

        for view in alpha_views:
            if view.endpoint not in endpoints:
                views.append(view)

        self.admin_db = Admin(
            self, name=self.get_config("name"), template_mode="bootstrap3"
        )
        self.admin_db.add_views(*views)

    def init_run(self):
        if self.__initiated:
            return
        host = self.conf.get("host")
        self.debug = (
            self.conf.get("debug")
            if not "ALPHA_DEBUG" in os.environ
            else (
                "y" in os.environ["ALPHA_DEBUG"].lower()
                or "t" in os.environ["ALPHA_DEBUG"].lower()
            )
        )
        if self.debug:
            sys.dont_write_bytecode = True
        self.log.info(
            f"Run api on host {host} port {self.port} {'DEBUG MODE' if self.debug else ''}"
        )
        self.__initiated = True

    def start(self):
        if self.pid is not None:
            return

        ssl_context = None
        if self.conf.get("ssl"):
            ssl_context = (self.conf.get("ssl_cert"), self.conf.get("ssl_key"))

        host = self.conf.get("host")
        threaded = self.conf.get("threaded")

        mode = self.conf.get("mode")
        if "ALPHA_API" in os.environ:
            mode = os.environ["ALPHA_API"]

        self.init_run()

        if mode == "wsgi":
            application = DebuggedApplication(self, True) if self.debug else self

            if host == "0.0.0.0" or host == "localhost" and os_lib.is_linux():
                host = ""
            self.log.info(
                f'Running {"debug " if self.debug else ""}WSGI mode on host <{host}> and port {self.port}'
            )

            server = WSGIServer(
                (host, self.port), application, log=self.log_requests.logger
            )
            server.serve_forever()
        else:
            watched_dirs = self.conf.get(
                "watched_dirs", default=[self.conf.get("project")]
            )
            os.environ["ALPHA_WATCHDIRS"] = ";".join(watched_dirs)
            reloader_type = self.conf.get("reloader_type", default="alpha")
            exlude_patterns = self.conf.get("exlude_patterns", default=[])
            exlude_patterns.extend(
                [
                    "*.vscode*",
                    "*site-packages*",
                    "*Anaconda3*",
                    "*Miniconda3*",
                    "*werkzeug*",
                    "*AppData*",
                    "*.zip*",
                ]
            )
            if reloader_type not in reloader_loops.keys():
                self.log.critical(
                    f"{reloader_type=} does not exist, it must be in {list(reloader_loops.keys())}"
                )
                return

            self.run(
                host=host,
                port=self.port,
                debug=self.debug,
                threaded=threaded,
                ssl_context=ssl_context,
                exclude_patterns=exlude_patterns,
                reloader_type=reloader_type,
            )

        # except SystemExit:
        #    self.info("API stopped")

    def stop(self, config_path=None):  # TODO: change
        if config_path is None:
            config_path = self.config_path
        if self.config_path is None:
            return

        # self.set_config(config_path=config_path, configuration=self.configuration)

        pid = self.get_config(["tmp", "process"])

        os.kill(pid, 9)

        self.log.info(f"Process n°{pid} killed")

    def get_config(self, name=""):
        if "/" in name:
            name = name.split("/")
        conf = self.conf.get(name)
        return conf

    def get_url(self, local=False, route: str = ""):
        if local:
            return f"http://localhost:{self.port}/{route}"
        ssl = self.get_config("ssl")
        pref = "https://" if ssl else "http://"
        return pref + self.get_config("host_public")

    def access_denied(self):
        self.get_current_route().access_denied()

    def get(self, name: str, default=None):
        route = self.get_current_route()
        if route is None:
            return None
        return route.get(name, default)

    def set(self, name: str, value):
        route = self.get_current_route()
        if route is None:
            raise AlphaException(f"Cannot find route to assign value {name=}={value}")
        return route.set(name, value)

    def __getitem__(self, key):
        return self.get(key)

    def error(self, message):
        if self.log is not None:
            self.log.error(message, level=4)

    def info(self, message):
        if self.log is not None:
            self.log.info(message, level=4)

    def warning(self, message):
        if self.log is not None:
            self.log.warning(message, level=4)

    def get_current_route(self) -> Route | None:
        """Return the current route.

        Returns:
            Route: [description]
        """
        request_uuid = AlphaRequest.get_uuid()
        try:
            full_path = request.full_path
        except:
            return None
        if request_uuid in self.routes_objects:
            return self.routes_objects[request_uuid]

        default_route = Route(
            uuid=request_uuid,
            route=full_path,
            parameters=[],
            request_state=request,
            api=self,
        )
        if request_uuid not in self.routes_objects:
            self.log.critical(f"Cannot get route for {request_uuid}")
            return default_route

        self.log.critical(f"Issue with route {request_uuid}")
        return default_route

    def get_path(self):
        return self.get_current_route().route

    def is_admin(self, check_logged_user: bool = True) -> bool:
        """Check if user is an admin or not.

        Args:
            log ([type], optional): [description]. Defaults to None.

        Returns:
            bool: [description]
        """
        # route = self.get_current_route()

        admin_password, admin_parameter = (
            self.conf.get("admins/password"),
            self["admin"],
        )
        if admin_parameter and admin_password is not None:
            if secure_lib.check_cry_operation_code(admin_parameter, admin_password):
                return True

        try:
            ip = request.remote_addr
        except:
            ## getting the hostname by socket.gethostname() method
            hostname = socket.gethostname()
            ## getting the IP address using socket.gethostbyname() method
            ip_address = socket.gethostbyname(hostname)
            ip = "127.0.0.1"
        admins_ips = self.conf.get("admins/ips")
        if admins_ips and (ip in admins_ips or f"::ffff:{ip}" in admins_ips):
            return True

        if check_logged_user:
            user = self.get_logged_user()
            if user is not None:
                if user.role >= 9:
                    return True
        return False

    def get_su_user(self, su_user_id: str, su_user_name: str):
        from ...models.user import AlphaUser

        admin_users = self.conf.get("admins/users")

        user = None
        if self.is_admin(check_logged_user=False) and su_user_id is not None:
            from ...libs import user_lib  # todo: modify

            if admin_users is not None and su_user_id is not None:
                u = [x for x in admin_users if ("id" in x and x["id"] == su_user_id)]
                user = u[0] if len(u) != 0 else None
                user = AlphaUser(**user)
            user = (
                user_lib.get_user_data_by_id(su_user_id, True) if user is None else user
            )

        if (
            user is None
            and self.is_admin(check_logged_user=False)
            and su_user_name is not None
        ):
            from ...libs import user_lib  # todo: modify

            if admin_users is not None and su_user_name is not None:
                u = [
                    x
                    for x in admin_users
                    if ("username" in x and x["username"] == su_user_name)
                ]
                user = u[0] if len(u) != 0 else None
                user = AlphaUser(**user)
            user = (
                user_lib.get_user_data_by_username(su_user_name, True)
                if user is None
                else user
            )
        return user

    def get_logged_user(self, algorithms=["HS256"]):
        from ...utils.api import ADMIN_USER_ID_PUBLIC, ADMIN_USER_NAME_PUBLIC
        from ...models.user import AlphaUser

        algorithms = list(algorithms)
        secret_key = self.config["JWT_SECRET_KEY"]

        user = None
        token = (
            AlphaRequest.get_token() if self.admin_token is None else self.admin_token
        )

        su_user_id, su_user_name = (
            self[ADMIN_USER_ID_PUBLIC.name],
            self[ADMIN_USER_NAME_PUBLIC.name],
        )

        if (
            self.is_admin(check_logged_user=False)
            and su_user_id is not None
            or su_user_name is not None
        ):
            user = self.get_su_user(su_user_id, su_user_name)
        elif token is not None:
            try:
                user_data_token = jwt.decode(token, secret_key, algorithms=algorithms)
            except:
                return None

            from ...libs import user_lib  # todo: modify

            user = user_lib.get_user_data_by_id(user_data_token["id"], True)
            if user is None and self.admin_token == token:
                return AlphaUser.map_from_token(user_data_token)  # TODO: modify

        perm_config = self.conf.get("auth/users", default={})
        if (
            user is not None
            and perm_config is not None
            and user.username in perm_config
            and "user_permissions" in perm_config[user.username]
        ):
            user.permissions.extend(perm_config[user.username]["user_permissions"])
        return user

    def is_get(self):
        return request.method == "GET"

    def is_post(self):
        return request.method == "POST"

    def is_put(self):
        return request.method == "PUT"

    def is_delete(self):
        return request.method == "DELETE"

    def is_patch(self):
        return request.method == "PATCH"

    def get_method(self):
        return request.method
