# CORE
from core import core

# MODULES
import re
from typing import Any
from sqlalchemy import MetaData

# MODELS
from ..models.main import AlphaException, AlphaCore

# UTILS
from ..utils.database import init as init_database_fct


def reoder_tables_and_binds_based_on_db_structure(
    tables: list[str], binds: list[str]
) -> tuple:
    db_structure = get_database_structure()

    s_binds, s_tables = [], []
    for bn in db_structure:
        tbls = get_tables_for_bind(bn)

        if binds is None or bn in [b.upper() for b in binds]:
            s_binds.append(bn)

        for t in tbls:
            if t in db_structure[bn]:
                if tables is None or t.upper() in tables:
                    s_tables.append(t)
    """if tables is None:
        s_tables = None
    if binds is None:
        s_binds = None"""
    return s_tables, s_binds


def init_databases(
    core: AlphaCore,
    tables: list[str] | None = None,
    binds: list[str] | None = None,
    create: bool = False,
    drop: bool = False,
    truncate: bool = False,
    force: bool = True,
    init: bool = False,
    init_views: bool = False,
    no_log: bool = False,
):
    """Initialise les bases de données en fonction des paramètres fournis. Cette fonction est la principale et appelle les autres fonctions pour effectuer diverses tâches.

    Args:
        core (AlphaCore): objet Core contenant les informations de base et les configurations
        tables (list[str] | dict[str, str], optional): Liste ou dictionnaire des noms des tables à traiter. Defaults to None.
        binds (list[str], optional): Liste des binds à traiter. Defaults to None.
        create (bool, optional): Booléen indiquant si les tables doivent être créées. Defaults to False.
        drop (bool, optional): Booléen indiquant si les tables doivent être supprimées. Defaults to False.
        truncate (bool, optional):  Booléen indiquant si les tables doivent être vidées. Defaults to False.
        force (bool, optional): Booléen indiquant si la configuration doit être forcée à 'local'. Defaults to True.
        init (bool, optional): Booléen indiquant si les fichiers d'initialisation doivent être traités. Defaults to False.
    """
    # Vérifie que la configuration est 'local' ou que le paramètre 'force' est True
    if core.configuration != "local" and not force:
        if core.log:
            core.log.error("Configuration must be <local>")
        return

    # Normalise le paramètre 'tables'
    tables = [t.upper() for t in tables] if tables is not None else None

    # Normalise le paramètre 'binds' et vérifie que les binds sont valides
    binds = init_database_fct.__normalize_and_check_binds(binds, core)

    tables, binds = reoder_tables_and_binds_based_on_db_structure(tables, binds)

    # Récupère les modèles de tables à partir des paramètres 'tables' et 'binds'
    tables_models = core.db.get_tables_models(tables, binds)

    # Filter views
    if not init_views:
        tables_models = [m for m in tables_models if not getattr(m, "__view__", False)]
        tables = [m.__tablename__ for m in tables_models]

    # Récupère et normalise la configuration d'initialisation des bases de données
    init_databases_config = init_database_fct.__get_normalized_init_config(core)

    # Initialise les bases de données en fonction des paramètres
    core.db.init_all(
        tables=tables_models,
        create=create,
        drop=drop,
        truncate=truncate,
        log=core.log,
        no_log=no_log,
    )

    # Charge les fichiers d'initialisation si le paramètre 'init' est True
    if init:
        init_database_fct.process_init_files(
            core, binds, tables, init_databases_config, no_log=no_log
        )


def get_table_content(
    bind: str,
    table: str,
    order_by: str,
    direction: str,
    page_index: int,
    page_size: int,
    limit: int | None = None,
):
    model = core.db.get_table_model(table, bind=bind)
    return core.db.select(
        model,
        page=page_index,
        per_page=page_size,
        order_by=order_by,
        order_by_direction=direction,
        limit=limit,
    )


def where_used(
    core: AlphaCore,
    data_type: str,
    value,
    bind: str,
    column_name: str | None = None,
) -> dict[str, Any]:
    """
    Find where a value is used in columns of a certain data type.

    :param core: AlphaCore instance to work with.
    :param data_type: Data type to search for in columns.
    :param value: Value to search for in columns.
    :param bind: Bind name to work with.
    :param column_name: Optional column name to match (default is None).
    :return: A dictionary containing table names, column names, and rows with matching values.
    """
    query = f"""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE data_type = '{data_type}';
    """
    outputs = {}
    results = core.db.get_query_results(query, bind=bind)

    outputs = __process_results(results, column_name, outputs)

    return __filter_matching_rows(core, bind, value, outputs)


def __process_results(results, column_name, outputs):
    """
    Process query results to filter columns by optional column_name.

    :param results: Query results.
    :param column_name: Optional column name to match.
    :param outputs: Dictionary to store processed outputs.
    :return: A dictionary containing table names and their filtered columns.
    """
    for r in results:
        if not r["table_name"] in outputs:
            outputs[r["table_name"]] = []

        if column_name is not None:
            matches = re.findall(column_name, r["column_name"])
            if len(matches) == 0:
                continue

        outputs[r["table_name"]].append(r["column_name"])

    outputs = {x: list(set(y)) for x, y in outputs.items() if len(y) != 0}
    return outputs


def __filter_matching_rows(core, bind, value, outputs):
    """
    Filter rows by matching value.

    :param core: AlphaCore instance to work with.
    :param bind: Bind name to work with.
    :param value: Value to search for in columns.
    :param outputs: Dictionary containing table names and their columns.
    :return: A dictionary containing table names, column names, and rows with matching values.
    """
    outputs_filtered = {}

    for table_name, columns in outputs.items():
        outputs_filtered[table_name] = {}

        for column in columns:
            query = f"""SELECT * FROM {table_name} WHERE {column} = {value}"""
            rows = core.db.get_query_results(query, bind=bind)

            if len(rows) != 0:
                outputs_filtered[table_name][column] = rows

    return outputs_filtered


def get_database_structure():
    # Crée une liste pour stocker les noms des tables enfants
    binds = list(core.db_cnx.keys())
    for bind in core.db.get_all_binds():
        if not bind in binds:
            binds.append(bind)

    bind_parent_tables = {}
    for bind in binds:
        if not bind in bind_parent_tables:
            bind_parent_tables[bind.upper()] = {}

        # Récupère les noms de toutes les tables de la base de données
        table_names = core.db.get_tables_names(bind=bind)

        # Parcourt toutes les tables de la base de données
        for table_name in table_names:
            if not table_name in bind_parent_tables[bind.upper()]:
                bind_parent_tables[bind.upper()][table_name] = []
            model = core.db.get_table_model(table_name)
            # Récupère les informations sur la table à partir de la base de données
            table = model.__table__  # metadata.tables[table_name]
            # Vérifie si la table a une clé étrangère faisant référence à la table "User"
            for foreign_key in table.foreign_keys:
                fk_name = foreign_key.column.table.name
                fk_bind = foreign_key.column.table.info.get("bind_key", None)

                if fk_bind == bind:
                    if not fk_name in bind_parent_tables[bind.upper()]:
                        bind_parent_tables[bind.upper()][fk_name] = []
                    bind_parent_tables[bind.upper()][fk_name].append(
                        {"bind": bind.upper(), "table": table_name}
                    )
                else:
                    if not fk_bind.upper() in bind_parent_tables:
                        bind_parent_tables[fk_bind.upper()] = {}
                    if not fk_name in bind_parent_tables[fk_bind.upper()]:
                        bind_parent_tables[fk_bind.upper()][fk_name] = []
                    bind_parent_tables[fk_bind.upper()][fk_name].append(
                        {"bind": bind.upper(), "table": table_name}
                    )

    for bind, tables in bind_parent_tables.items():
        names = sorted(tables, key=lambda k: len(tables[k]), reverse=True)
        bind_parent_tables[bind] = {name: tables[name] for name in names}

    return bind_parent_tables


def get_tables_for_bind(bind):
    tables = []
    visited_tables = set()

    # Fonction récursive pour parcourir les tables en prenant en compte les dépendances
    def traverse(table):
        if table not in visited_tables:
            visited_tables.add(table)
            model = core.db.get_table_model(table)
            for foreign_key in model.__table__.foreign_keys:
                dependent_table = foreign_key.target_fullname.split(".")[0]
                traverse(dependent_table)
            tables.append(table)

    # Appelle la fonction traverse pour chaque table de la liaison de base de données
    for table in core.db.get_tables_names(bind=bind):
        traverse(table)

    return tables
