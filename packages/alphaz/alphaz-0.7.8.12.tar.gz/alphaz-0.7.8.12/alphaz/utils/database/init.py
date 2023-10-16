# MODULES
import glob, os, importlib, re, ujson, pathlib

# MODELS
from ...models.main import AlphaException, AlphaCore

INI_TYPES = {
    "json": {"key": "init_database_dir_json", "pattern": "*.json"},
    "py": {"key": "init_database_dir_py", "pattern": "*.py"},
    "sql": {"key": "init_database_dir_sql", "pattern": "*.sql"},
}


def __get_module_path(file_path: str) -> str:
    """
    Convert a file path to a Python module path.

    :param file_path: File path to convert.
    :return: The corresponding module path.
    """
    current_path = os.getcwd()
    module_path = (
        file_path.replace(current_path, "")
        .replace("/", ".")
        .replace("\\", ".")
        .replace(".py", "")
    )

    if module_path[0] == ".":
        module_path = module_path[1:]

    return module_path


def __process_sql_file(core: AlphaCore, bind: str, file_path: str) -> None:
    """
    Process an SQL file for database initialization.

    :param core: AlphaCore instance to work with.
    :param bind: Bind name to work with.
    :param file_path: Path to the SQL file containing the database initialization statements.
    :raises AlphaException: If there is any issue with the provided file.
    """
    with open(file_path, "r") as f:
        sql = f.read()
        sql = replace_to_date(sql)
        statements = sql.split(";")

        for statement in statements:
            try:
                core.db.execute(statement + ";", bind=bind.upper())
            except Exception as ex:
                print(f"Error with init of {file_path=}: " + str(ex))
                core.db.log.error(f"Error with init of {file_path=}", ex=ex)


def __process_headers_values(
    core: AlphaCore,
    bind: str,
    table_name: str,
    table,
    headers: list[str],
    values: list[str | dict],
    data_type: str = "alpha",
) -> None:
    """
    Process headers and values for a given table.

    :param core: AlphaCore instance to work with.
    :param file_path: Path to the file containing the database initialization configuration.
    :param bind: Bind name to work with.
    :param table_name: Name of the table to process.
    :param table: Table object to process.
    :param headers: list of header names.
    :param values: list of values for the table.
    :param data_type: Type of data being processed (default is "alpha").
    :raises ValueError: If an invalid data_type is provided.
    """
    if not isinstance(values, list):
        core.log.error(
            f'"values" key from {table_name=} and {bind=} must be of type <list>'
        )
        return

    if not isinstance(headers, list):
        core.log.error(
            f'"headers" key from {table_name=} and {bind=} must be of type <list>'
        )
        return

    entries = __extract_entries(core, bind, table_name, values, data_type)

    if entries:
        core.db.process_entries(bind, table, headers=headers, values=entries)


def __extract_entries(
    core: AlphaCore,
    bind: str,
    table_name: str,
    values: list[str | dict],
    data_type: str,
) -> list[list[str]]:
    """
    Extract entries from the given values based on the data type.

    :param core: AlphaCore instance to work with.
    :param file_path: Path to the file containing the database initialization configuration.
    :param bind: Bind name to work with.
    :param table_name: Name of the table to process.
    :param values: list of values for the table.
    :param data_type: Type of data being processed.
    :return: list of extracted entries.
    :raises ValueError: If an invalid data_type is provided.
    """
    entries = []

    for entry in values:
        if data_type == "alpha":
            if not isinstance(entry, list):
                core.log.error(
                    f"{table_name=} and {bind=} entries must be of type <list>"
                )
                continue
        elif data_type == "sql":
            if not isinstance(entry, dict):
                core.log.error(
                    f"{table_name=} and {bind=} entries must be of type <dict>"
                )
                continue
            entry = list(entry.values())
            if len(entry) == 0:
                continue
        else:
            raise ValueError(f"Invalid data_type '{data_type}'")

        entries.append(entry)

    return entries


def get_init_files(
    core: AlphaCore, binds: list[str], init_databases_config: dict
) -> list[str]:
    ini_files = set()
    for bind in binds:
        if not bind in init_databases_config:
            core.log.warning(
                f"No initialisation configuration has been set in <databases> entry for {bind=}"
            )
            continue

        bind_cf = init_databases_config[bind]
        if type(bind_cf) == str and bind_cf.upper() in init_databases_config:
            bind_cf = init_databases_config[bind_cf.upper()]

        for ini_type, cf_ini in INI_TYPES.items():
            if not cf_ini["key"] in bind_cf:
                continue

            ini_dir = bind_cf[cf_ini["key"]]
            files = glob.glob(ini_dir + os.sep + cf_ini["pattern"])
            ini_files.update(files)

            if ini_type == "sql":
                for file_path in files:
                    __process_sql_file(core, bind, file_path)
    return ini_files


def process_init_files(
    core: AlphaCore,
    binds: list[str],
    tables: list[str],
    init_databases_config: dict,
    no_log: bool = False,
):
    """Charge les fichiers d'initialisation en fonction des types de fichiers et du répertoire d'initialisation spécifié pour chaque type.

    Args:
        core (AlphaCore): objet Core contenant les informations de base et les configurations
        binds (list[str]): Liste des binds à traiter
        tables (list[str]):  Liste ou dictionnaire des noms des tables à traiter. Defaults to None.
        init_databases_config (dict): Dictionnaire de configuration d'initialisation normalisé avec les clés en majuscules
    """
    tables_configs = {}  # TODO add BIND
    for file_path in get_init_files(core, binds, init_databases_config):
        ini = {}

        ini_type = pathlib.Path(file_path).suffix.replace(".", "")
        if ini_type == "py":
            module_path = __get_module_path(file_path)
            module = importlib.import_module(module_path)

            if not hasattr(module, "ini"):
                continue

            ini = module.__dict__["ini"]
            if type(ini) != dict:
                raise AlphaException(
                    f"In file {file_path} <ini> configuration must be of type <dict>"
                )
        elif ini_type == "json":
            if os.path.exists(file_path):
                try:
                    with open(file_path, encoding="utf-8") as json_data_file:
                        ini = ujson.load(json_data_file)
                except Exception as ex:
                    raise AlphaException(f"Cannot read file {file_path}: {ex}")
        elif ini_type == "sql":
            continue
        else:
            raise ValueError(f"Unsupported file type '{ini_type}'")

        for table_name, conf in ini.items():
            if not table_name in tables:
                continue
            if not table_name in tables_configs:
                tables_configs[table_name] = []

            if not isinstance(conf, dict):
                core.log.error(
                    f"Configuration for {table_name=} in file {file_path} must be of type <dict>",
                    enabled=not no_log,
                )
                continue
            conf["file_name"] = file_path
            tables_configs[table_name].append(conf)

    for table_name in tables:
        if not table_name in tables_configs:
            continue

        for configuration in tables_configs[table_name]:
            model = core.db.get_table_model(table_name)
            bind = model.__bind_key__.upper()
            file_name = configuration["file_name"]

            entries = configuration.get("objects", [])
            if entries:
                core.db.process_entries(bind, model, values=entries)
                core.log.info(
                    f"{table_name=} and {bind=} initiatied with <objects> format with file {file_name}",
                    enabled=not no_log,
                )

            headers, values = configuration.get("headers", []), configuration.get(
                "values", []
            )
            if len(values) != 0:
                __process_headers_values(core, bind, table_name, model, headers, values)
                core.log.info(
                    f"{table_name=} and {bind=} initiatied with <values> format with file {file_name}",
                    enabled=not no_log,
                )

            values = configuration.get("results", [{"items": [{}]}])[0]["items"]
            headers = list(values[0].keys())
            if len(values) != 0:
                __process_headers_values(
                    core, bind, table_name, model, headers, values, "sql"
                )
                core.log.info(
                    f"{table_name=} and {bind=} initiatied with <results> format with file {file_name}",
                    enabled=not no_log,
                )


def __normalize_and_check_binds(binds: list[str], core: AlphaCore) -> list[str]:
    """Normalise le paramètre 'binds' et vérifie que les binds sont valides.

    Args:
        binds (list[str]): Liste des binds à traiter
        core (AlphaCore): objet Core contenant les informations de base et les configurations

    Raises:
        AlphaException: _description_

    Returns:
        list[str]: Liste contenant la liste des binds normalisés et la liste des binds récupérés depuis l'objet Core
    """
    db_binds = core.db.get_all_binds()
    binds = [bind.upper() for bind in binds] if binds is not None else db_binds
    if len(binds) != len(db_binds):
        for bind in binds:
            if not bind in db_binds:
                raise AlphaException(f"Cannot find {bind=}")
    return binds


def __get_normalized_init_config(core: AlphaCore) -> dict[str, dict]:
    """Récupère et normalise la configuration d'initialisation des bases de données.

    Args:
        core (AlphaCore): objet Core contenant les informations de base et les configurations

    Raises:
        AlphaException: _description_

    Returns:
        dict[str, dict]: Dictionnaire de configuration d'initialisation normalisé avec les clés en majuscules
    """
    init_databases_config: dict = core.config.get("databases")
    if init_databases_config is None:
        raise AlphaException(
            "No initialisation configuration has been set in <databases> entry"
        )
    return {x.upper(): y for x, y in init_databases_config.items()}


def replace_to_date(sql: str) -> str:
    """
    Replace TO_DATE function calls in an SQL string with strftime calls.

    :param sql: SQL string to process.
    :return: SQL string with TO_DATE calls replaced by strftime calls.
    """
    matchs = re.findall(r"to_date\('[^']+','[^']+'\)", sql)
    for match in matchs:
        date = match.replace("to_date(", "").split(",")[0]
        format = match.split(",")[1].replace(")", "")
        sql = sql.replace(match, f"strftime({format}, {date})")
    return sql
