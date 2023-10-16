# MODULES
import inspect, requests, json

# UTILS
from ..utils.api import ROUTES

# MODELS
from ..models.logger import AlphaLogger
from ..models.api import ApiMethods
from ..models.main import AlphaException
from ..models.api._answer import ApiAnswer, ApiPagination

# LIBS
from ..libs import dict_lib, json_lib, py_lib

# CORE
from .. import timer

MODULES = {}


def get_api_answer(
    url: str,
    params: dict = {},
    log: AlphaLogger | None = None,
    no_log: bool = False,
    method: ApiMethods = ApiMethods.GET,
    requester=None,
    allow_none: bool = False,
    token: str | None = None,
) -> ApiAnswer | None:
    """Get data from api

    Args:
        url (str): [description]
        params (dict, optional): [description]. Defaults to {}.
        log (AlphaLogger, optional): [description]. Defaults to None.
        method (ApiMethods, optional): The request method. Defaults to GET.
        data_only (bool, optional): return only the data. Default to True.

    Returns:
        dict: The request result
    """
    from core import core

    stack = inspect.stack()[1]
    requester = requester or py_lib.get_project_name_from_stack(stack)

    fct = requests.get
    method_str = (
        str(method).lower() if not hasattr(method, "name") else method.name.lower()
    )
    if hasattr(requests, method_str):
        fct = getattr(requests, method_str)

    converted_params = {}
    for key, value in params.items():
        if value is None and not allow_none:
            continue
        if type(value) == list:
            converted_params[key] = (
                "["
                + ";".join(
                    [
                        json_lib.jsonify_data(x, string_output=True)
                        if x is not None
                        else ""
                        for x in value
                    ]
                )
                + "]"
            )
        else:
            converted_params[key] = json_lib.jsonify_data(value, string_output=True)

    headers = {}
    if token is not None or core.api.admin_token is not None:
        token = core.api.admin_token if token is None else token
        headers["Authorization"] = f"Bearer {token}"

    if not "http" in url:
        url = f"http://localhost:{core.api.port}/{url}"
    converted_params["requester"] = requester
    if no_log:
        converted_params["no_log"] = "Y"
    try:
        if method_str.lower() == "post":
            resp = fct(url=url, data=converted_params, headers=headers)
        else:
            resp = fct(url=url, params=converted_params, headers=headers)
    except Exception as ex:
        raise AlphaException(f"Fail to contact {url}", ex=ex)

    try:
        answer = resp.json()
    except Exception as ex:
        raise AlphaException(f"Cannot decode answer from {url=}", ex=ex)

    if (
        type(answer) == dict
        and answer.get("status", None) is not None
        and answer.get("status_description", None) is not None
    ):
        api_answer = ApiAnswer.map_from_dict(answer)
    else:
        api_answer = ApiAnswer.map_from_dict(
            {
                "data": answer,
                "token_status": resp.headers.get("x-token-status"),
                "status": resp.headers.get("x-status"),
                "status_code": resp.status_code,
                "error": int(resp.headers.get("x-error")),
                "warning": int(resp.headers.get("x-warning")),
                "status_description": resp.headers.get("x-status-description"),
                "requester": resp.headers.get("x-requester"),
            }
        )

    pagination = resp.headers.get("x-pagination", {})
    if isinstance(pagination, str):
        pagination_dict = json.loads(pagination.replace("'", '"'))
        pagination = ApiPagination.map_from_dict(pagination_dict)
    api_answer.pagination = pagination
    return api_answer


def get_api_data(
    url: str,
    params: dict = {},
    log: AlphaLogger | None = None,
    method: ApiMethods = ApiMethods.GET,
    data_only: bool = True,
    requester=None,
) -> dict | ApiAnswer:
    """Get data from api

    Args:
        url (str): [description]
        params (dict, optional): [description]. Defaults to {}.
        log (AlphaLogger, optional): [description]. Defaults to None.
        method (ApiMethods, optional): The request method. Defaults to GET.
        data_only (bool, optional): return only the data. Default to True.

    Returns:
        dict: The request result
    """
    answer = get_api_answer(
        url=url, params=params, log=log, method=method, requester=requester
    )

    if answer.error:  # TODO: check if raised
        raise AlphaException(
            f"Fail to get data from {url}: {answer.status} - {answer.status_description}"
        )

    return answer.data if data_only else answer


def get_routes_infos(
    log: AlphaLogger | None = None, categories=None, routes=None, reload_=False
) -> dict:
    """Get all apis routes with informations.

    Args:
        log ([AlphaLogger], optional): [description]. Defaults to None.
    Args:
        log ([AlphaLogger], optional): [description]. Defaults to None.

    Returns:
        dict: [description]
    """
    global ROUTES
    if len(MODULES) != 0 and not reload_:
        return MODULES

    if log:
        log.debug(
            f"Getting {'alphaz' if not all else 'all'} routes from loaded modules"
        )

    routes_dict = {}

    for path, cg in ROUTES.items():
        out = dict_lib.get_nested_dict_from_list(cg["paths"])
        routes_dict = dict_lib.merge_dict(routes_dict, out)
    categories = list(set([x["category"] for x in ROUTES.values()]))
    categories.sort()

    routes_dict = dict_lib.sort_dict(routes_dict)

    MODULES["routes_list"] = ROUTES.keys()
    MODULES["routes"] = ROUTES
    MODULES["routes_paths"] = routes_dict
    MODULES["categories"] = categories
    MODULES["categories_routes"] = {
        c: [x for x, y in ROUTES.items() if y["category"] == c] for c in categories
    }
    return MODULES
