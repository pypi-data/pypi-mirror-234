from ...utils.api import route, Parameter, ParameterMode

from ...libs import logs_lib, database_lib

from ...models.main import AlphaException


from core import core

API = core.api
DB = core.db
log = core.get_logger("api")


@route("/schemas", parameters=[Parameter("name")])
def get_schemas():
    return database_lib.get_schemas(**API.gets())


@route(
    "/database/tables",
    parameters=[
        Parameter("binds", ptype=list[str]),
        Parameter("tables", ptype=list[str]),
    ],
    admin=True,
)
def liste_tables():
    return DB.get_tables_models(**API.gets())


@route("/database/tables/names", parameters=[Parameter("bind")], admin=True)
def liste_tables_names():
    return DB.get_tables_names(**API.gets())


@route(
    "/database/create",
    admin=True,
    parameters=[
        Parameter("bind"),
        Parameter("table", required=True),
        Parameter("drop", ptype=bool),
    ],
)
def create_table():
    return core.create_table(**API.gets())


@route(
    "/database/drop",
    admin=True,
    parameters=[Parameter("bind"), Parameter("table", required=True)],
)
def drop_table():
    return core.db.drop_table(**API.gets())


DB_INIT_PARAMETERS = [
    Parameter("binds", ptype=list[str]),
    Parameter("tables", ptype=list[str]),
    Parameter("drop", ptype=bool, default=False),
    Parameter("truncate", ptype=bool, default=False),
    Parameter("force", ptype=bool, default=False),
    Parameter("create", ptype=bool, default=False),
    Parameter("init", ptype=bool, default=False),
    Parameter("init_views", ptype=bool, default=False),
]


@route(
    "/database/init",
    admin=True,
    parameters=DB_INIT_PARAMETERS,
)
def init_all_database():
    database_lib.init_databases(core, **API.gets())


@route("database/blocking", admin=True)
def get_blocking_queries():
    return core.db.get_blocked_queries()


@route(
    "/table",
    parameters=[
        Parameter("bind", ptype=str, default="ALPHA"),
        Parameter("table", ptype=str, required=True),
        Parameter("order_by", ptype=str),
        Parameter("direction", ptype=str),
        Parameter("page_index", ptype=int),
        Parameter("page_size", ptype=int),
        Parameter("limit", ptype=int),
    ],
    logged=True,
)
def get_transactions_history():
    return database_lib.get_table_content(**API.gets())


@route(
    "/table/columns",
    parameters=[
        Parameter("bind", ptype=str, default="ALPHA"),
        Parameter("table", ptype=str, required=True),
    ],
)
def get_table_columns():
    return core.db.get_table_columns(**API.gets())


@route(
    "/table/model",
    parameters=[
        Parameter("bind", ptype=str, default="ALPHA"),
        Parameter("table", ptype=str, required=True),
    ],
)
def get_table_model():
    return core.db.get_table_model(**API.gets()).get_table_model_structure()


@route(
    "/database/whereused",
    parameters=[
        Parameter("data_type", required=True),
        Parameter("value", required=True),
        Parameter("bind", required=True),
        Parameter("column_name"),
    ],
)
def get_database_whereused():
    return database_lib.whereused(**API.gets())


@route("/database/structure")
def get_database_structure():
    return database_lib.get_database_structure(**API.gets())
