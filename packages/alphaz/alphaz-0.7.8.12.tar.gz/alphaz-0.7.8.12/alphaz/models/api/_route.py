import datetime, os, copy, ujson, json
import time
import traceback

from flask import (
    jsonify,
    request,
    make_response,
    render_template,
    send_from_directory,
)

from ...libs.time_lib import timer

from ...libs import json_lib, converter_lib, io_lib, py_lib
from ...models.main import AlphaException
from ...models.api import ApiAnswer, AlphaRequest
from ...models.json._converters import AlphaJSONEncoder

from ._parameter import Parameter
from ..main._exception import get_message_from_name

SEPARATOR = "__"
DEBUG = False


def get_columns_values_output(
    objects: list, columns: list | None = None, header: bool = False
) -> dict:
    """Generate columns names output columns names + list of list (only the values) + nb of values if not header
    ex : { "columns":["col1","col2",...], "values": ["value1","value2",..], "values_nb":12}

    else Generate columns names output columns names + list of JSON objetcs + nb of values,

    ex : { "columns":["col1","col2",...], "values": [{"col1": "value1",...},{...}], "values_nb":12}

    Args:
        objects (list): [description]

    Args:
        objects (list): [description]
        columns (list): [description]
        header (bool): [Add headers to values]

    Returns:
        dict: [description]
    """
    if len(objects) == 0:
        return {"columns": [], "values": [], "values_nb": 0}

    results = json_lib.jsonify_data(objects)

    if columns and len(columns) != 0 and len([x for x in columns if x != ""]) != 0:
        results = [
            {key: value for key, value in result.items() if key in columns}
            for result in results
        ]
    else:
        columns = list(results[0].keys())
    if header:
        return {"columns": columns, "values": results, "values_nb": len(results)}

    data = {}
    data["columns"] = [x for x in columns if x in results[0]]
    data["values"] = [[x[y] for y in columns if y in x] for x in results]
    data["values_nb"] = len(data["values"])
    return data


def check_format(data, depth=3):
    if depth == 0:
        return True

    accepted = [int, str, float]
    if type(data) in accepted:
        return True

    if type(data) == list and len(data) != 0:
        return check_format(data[0], depth - 1)
    if type(data) == dict and len(data) != 0:
        return check_format(list(data.keys())[0], depth - 1) & check_format(
            list(data.values())[0], depth - 1
        )
    return False


def description_from_status(message: str):
    return get_message_from_name(message)


class Route:
    no_log = False
    ex = None

    def __init__(
        self,
        uuid: str,
        route: str,
        parameters: list[Parameter],
        request_state,
        api,
        cache: bool = False,
        logged: bool = False,
        admin: bool = False,
        timeout=None,
        description: str = "",
        mode=None,
    ):
        self.__timeout = timeout
        self.uuid: str = uuid
        self.route: str = route
        self.cache: bool = cache
        self.logged: bool = logged
        self.admin: bool = admin
        self.description = description

        self.api = api
        self.jwt_secret_key = (
            "" if not "JWT_SECRET_KEY" in api.config else api.config["JWT_SECRET_KEY"]
        )

        self.full_path = request_state.full_path
        self.files = request.files

        self.args = request_state.args
        self.form = request.form
        try:
            self.json = AlphaRequest.get_json()
        except:
            self.json = None
        self.dict = request.args.to_dict(flat=False)

        self.mode = mode.lower() if mode != None else "data"

        self.lasttime = datetime.datetime.now()

        self.data = {}
        self.returned = {}

        self.html = {"page": None, "parameters": None}
        self.message = "No message"

        self.file_to_get = (None, None)
        self.file_to_set = (None, None)

        self.cache_dir = api.cache_dir
        self.log = api.log
        self.method = request_state.method

        self.page: int = 0
        self.total, self.total_pages, self.per_page = None, None, None
        self._is_pagination: bool | None = None

        self.init_return()

        self.parameters: dict[str, Parameter] = {
            y.name: copy.copy(y) for y in parameters
        }
        for parameter in self.parameters.values():
            try:
                parameter.set_value(self.dict, self.json, self.form, self.args)
                if parameter.name == "no_log":
                    self.no_log = parameter.value
                else:
                    parameter.no_log = self.no_log
            except Exception as ex:
                # TODO: enhance
                message = traceback.format_exc()
                self.set_error(status=message, ex=ex)
                self.ex = ex
                return

    def is_outdated(self):
        return (datetime.datetime.now() - self.lasttime).total_seconds() > 60 * 5

    def get(self, name, default=None, enable_none: bool = False):
        if not name in self.parameters:
            return default

        parameter = self.parameters[name]
        value = None if parameter is None else parameter.value
        if not enable_none and value is None:
            value = default
        return value

    def set(self, name, value):
        if not name in self.parameters:
            raise AlphaException(f"{name} is not a parameter or route {self.route}")

        parameter = self.parameters[name]
        parameter._value = value

    def __getitem__(self, key):
        return self.get(key)

    def is_time(self, timeout):
        is_time = False
        if timeout is not None:
            now = datetime.datetime.now()
            lastrun = self.lasttime
            nextrun = lastrun + datetime.timedelta(minutes=timeout)
            is_time = now > nextrun
        return is_time

    def keep(self):
        if not self.cache:
            return False
        reset_cache = self.get("reset_cache") or self.is_time(self.__timeout)
        if reset_cache:
            return False
        return self.is_cache()

    def get_key(self):
        route = self.route if not self.route[0] == "/" else self.route[1:]
        key = f"{route}__"
        for name, parameter in self.parameters.items():
            if parameter.cacheable and not parameter.private:
                key += f"{parameter.name}-{parameter.value}_"
        return key

    def get_cache_path(self):
        if self.cache_dir is None:
            return None
        key = self.get_key()
        cache_path = self.cache_dir + os.sep + key + ".cache"
        return cache_path

    def is_cache(self):
        cache_path = self.get_cache_path()
        if cache_path is None and not self.no_log:
            self.log.error("Cache path does not exist")
            return False
        return os.path.exists(cache_path)

    def set_cache(self):
        self.lasttime = datetime.datetime.now()
        cache_path = self.get_cache_path()
        if cache_path is None and not self.no_log:
            self.log.error("cache path does not exist")
            return
        try:
            returned = io_lib.archive_object(self.data, cache_path)
        except Exception as ex:
            if not self.no_log:
                self.log.error(f"Cannot cache route {self.get_key()}: {str(ex)}")

    def get_cached(self):
        if self.log and not self.no_log:
            self.log.info(f"GET cache for {self.route}")

        if self.is_cache():
            cache_path = self.get_cache_path()
            data = io_lib.unarchive_object(cache_path)
            if data:
                self.init_return()
                self.set_data(data)
                return True
        return False

    def set_status(self, status="success", description=None):
        self.returned.status = str(status) if status is not None else "success"
        self.returned.status_description = (
            description
            if description is not None
            else description_from_status(self.returned.status)
        )

    def get_status(self) -> tuple[str, str]:
        return (self.returned.status, self.returned.status_description)

    def timeout(self):
        self.returned.status = "timeout"
        self.returned.status_description = description_from_status(self.returned.status)
        self.returned.status_code = 524
        self.returned.error = 1

    def access_denied(self, description: str | None = None):
        self.returned.status = "unauthorized"
        self.returned.status_description = (
            description_from_status(self.returned.status)
            if description is None
            else description
        )
        self.returned.token_status = "denied"
        self.returned.error = 1
        self.returned.status_code = 401

    def is_error(self) -> bool:
        return self.returned.error

    def is_warning(self) -> bool:
        return self.returned.warning

    def set_error_not_logged(self):
        self.returned.status = "not_logged"
        self.returned.status_description = description_from_status(self.returned.status)
        self.returned.token_status = "denied"
        self.returned.error = 1
        self.returned.status_code = 401

    def set_error(
        self,
        status: str | AlphaException = "error",
        description: str | None = None,
        warning: int = 0,
        error_code: int = 520,
        ex=None,
    ):
        log_fct = self.log.error if warning == 0 else self.log.warning

        if isinstance(status, AlphaException):
            ex = status
            status = "error"
        if type(status) == "str" and ("Traceback" in status or "\n" in status):
            description = status
            status = "error"
        if isinstance(ex, AlphaException):
            warning = ex.warning
            description = ex.description
            status = (
                ex.name if ex.name.lower() != ex.description.lower() else "exception"
            )
            # description += "Exception\n" + "\n".join(ex.traces)
            if not self.no_log:
                log_fct(f"{status} - {description}", level=2)
        elif not self.no_log:
            if description is None:
                description = ""
            if ex is not None:
                description += f"\n\n{ex}"
            log_fct(f"{status} - {description}", level=2)

        self.mode == "data"
        self.returned.status = str(status)
        self.returned.status_code = error_code if not warning else 200
        self.returned.status_description = (
            str(description)
            if description
            else description_from_status(self.returned.status)
        )
        self.returned.error = 1 if warning == 0 else 0
        self.returned.warning = int(warning)

    def set_warning(
        self,
        status: str | AlphaException = "warning",
        description: str | None = None,
    ):
        self.set_error(status=status, description=description, warning=1)

    def print(self, message):
        self.mode == "print"
        self.message = message

    def init_return(self):
        self.file_to_get = (None, None)
        self.file_to_set = (None, None)
        self.returned, self.data = ApiAnswer(), {}

    def set_data(self, data):
        self.mode == "data"
        self.data = data

    def set_file(self, directory, filename):
        self.mode = "set_file"
        self.file_to_set = (directory, filename)

    def get_file(self, directory, filename, as_attachment=True):
        self.mode = "get_file" if not as_attachment else "get_file_attached"
        self.file_to_get = (directory, filename)

    def set_html(self, page, parameters={}):
        self.mode = "html"
        self.data = {"page": page, "parameters": parameters}

    def is_paginated(self):
        return (
            self.parameters.get("page", None) is not None
            and self.parameters.get("per_page", None) is not None
        )

    def is_pagination(self) -> bool:
        if self._is_pagination is None:
            pagination_mode = self.api.db.config.get("pagination_mode", "standard")
            if pagination_mode == "standard":
                is_pagination = self.api.db.full_count is not None
            else:
                is_pagination = self.page is not None and (
                    py_lib.is_list(self.data)
                    and len(self.data) == 2
                    and type(self.data[0]) == list
                    and type(self.data[1]) == int
                )
            self._is_pagination = is_pagination
            return is_pagination
        return self._is_pagination

    def set_pagination(self):
        format_ = self.get_format()
        data = {} if self.data is None else self.data
        self.total, self.total_pages, self.page, self.per_page = (
            None,
            None,
            self.get("page", 0),
            self.get("per_page", None),
        )

        is_pagination = self.is_pagination()
        pagination_mode = self.api.db.config.get("pagination_mode", "standard")
        if pagination_mode == "standard":
            if is_pagination and py_lib.is_iterable(data):
                self.per_page = len(data) if self.per_page is None else self.per_page
                self.total = (
                    self.api.db.full_count if self.api.db.full_count is not None else 0
                )
                self.total_pages = (
                    int(self.total / self.per_page)
                    if self.per_page is not None and self.per_page != 0
                    else 0
                )
        else:
            if self.per_page is None and is_pagination:
                self.per_page = len(data[0])

            if not "inpagination" in format_ and is_pagination:
                self.total, self.total_pages = (
                    data[1] if data[1] is not None else 0,
                    int(data[1] / self.per_page) if self.per_page is not None else 0,
                )
                data = data[0]
            self.data = data

    def get_headers(self):
        format_ = self.get_format()
        headers = {}
        if "txt" in format_:
            headers["Content-Type"] = "text/txt; charset=utf-8"
        elif "xml" in format_:
            headers["Content-Type"] = "text/xml; charset=utf-8"

        headers_content = {
            "X-token-status": self.returned.token_status,
            "X-status": self.returned.status,
            "X-error": self.returned.error,
            "X-warning": self.returned.warning,
            "X-status-description": self.returned.status_description,
            "X-requester": self.returned.requester,
        }
        for key, value in headers_content.items():
            headers[key] = value
        headers[
            "Access-Control-Expose-Headers"
        ] = "*"  # ",".join(headers_content.keys())
        # headers["Access-Control-Allow-Headers"] = "*" # ",".join(headers_content.keys())

        # returned = Response(returned, status=returned["status_code"])
        if self.is_pagination():
            headers["X-pagination"] = json.dumps(
                {
                    "total": self.total,
                    "total_pages": self.total_pages,
                    "page": self.page,
                    "previous_page": self.page - 1 if self.page > 0 else 0,
                    "next_page": (
                        self.page + 1
                        if self.page < self.total_pages
                        else self.total_pages
                    )
                    if (self.total_pages is not None and self.page is not None)
                    else None,
                    "per_page": self.per_page,
                }
            )

        return headers

    def get_format(self) -> str:
        default_format = self.api.conf.get("default_format", "standard")
        format_ = self.get("format", default=default_format, enable_none=False).lower()
        return format_

    def get_return(self, forceData=False, return_status=None):
        format_ = self.get_format()

        if self.mode == "html":
            if "page" in self.data:
                return render_template(self.data["page"], **self.data["parameters"])
            else:
                return self.data
        elif self.mode == "print":
            return self.message
        elif "get_file" in self.mode:
            directory, filename = self.file_to_get
            if directory is not None and filename is not None:
                if not self.no_log:
                    self.log.info(f"Sending file {filename} from {directory}")
                try:
                    return send_from_directory(
                        directory,
                        filename,
                        as_attachment="attached" in self.mode,
                    )
                except FileNotFoundError:
                    self.set_error("missing_file")
            else:
                self.set_error("missing_file")

        if isinstance(self.data, Exception):
            if hasattr(self.data, "msg"):
                self.set_error(self.data.msg, self.data.msg)
            elif hasattr(self.data, "args"):
                self.set_error(self.data.args[0], self.data.args[0])
            self.data = {}

        self.returned.data = {}

        self.set_pagination()

        data = self.data
        if "check" in format_ and not check_format(data):
            tic = time.perf_counter()
            data = json_lib.jsonify_data(data)
            toc = time.perf_counter()
            elapsed_time = toc - tic
            if DEBUG:
                print(f"Elapsed time: {elapsed_time:0.4f} seconds for jsonify_data")

        if "table" in format_:
            data = get_columns_values_output(
                data, self.get("columns"), header="header" in format_
            )

        self.returned.data = data
        status_code = self.returned.status_code
        if type(self.returned.status) == int:
            status_code = self.returned.status

        tic = time.perf_counter()

        returned = None
        route_output = (
            data if not "integrated" in format_ else self.returned
        )  # if "make" in format_ else ujson.dumps(data)

        if "xml" in format_:
            route_output = json_lib.jsonify_data(route_output)
            route_output = converter_lib.dict_to_xml(
                route_output, attr_type=not "no_type" in format_
            )
        elif "txt" in format_:
            if type(route_output) != str:
                route_output = json.dumps(route_output, cls=AlphaJSONEncoder)
            route_output = str(route_output)
            if (
                route_output is not None
                and len(route_output) != 0
                and route_output[0] == '"'
            ):
                route_output = route_output[1:-1]
        elif "jsonify" in format_:
            returned = jsonify(route_output)
        else:
            route_output = json.dumps(route_output, cls=AlphaJSONEncoder)

        toc = time.perf_counter()
        elapsed_time = toc - tic
        if DEBUG:
            print(f"Elapsed time: {elapsed_time:0.4f} seconds for conversion")

        tic = time.perf_counter()

        if returned is None:
            if "make" in format_:
                returned = make_response(route_output, status_code)
            else:
                returned = make_response({}, status_code)
                returned.set_data(route_output)

        toc = time.perf_counter()
        elapsed_time = toc - tic
        if DEBUG:
            print(f"Elapsed time: {elapsed_time:0.4f} seconds for returned")

        headers = self.get_headers()

        for key, value in headers.items():
            returned.headers[key] = (
                ujson.dumps([str(v) for v in value.split("\n")])
                if "\n" in str(value)
                else value
            )
        return returned

    def log_user(self, user):
        self.returned.role = "user"
        if user.role >= 9:
            self.returned.role = "admin"
        self.returned.token = jwt.encode(
            {
                "username": user.username,
                "id": user.id,
                "time": str(datetime.datetime.now()),
            },
            self.jwt_secret_key,
            algorithm="HS256",
        ).decode("utf-8")
        self.returned.valid_until = datetime.datetime.now() + datetime.timedelta(days=7)
